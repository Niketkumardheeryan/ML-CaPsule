import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:fl_chart/fl_chart.dart';
import '../providers/bitcoin_provider.dart';
import '../widgets/custom_card.dart';

class ChartScreen extends StatefulWidget {
  const ChartScreen({super.key});

  @override
  State<ChartScreen> createState() => _ChartScreenState();
}

class _ChartScreenState extends State<ChartScreen> {
  int _limit = 100;

  @override
  void initState() {
    super.initState();
    // Load historical data when screen is created
    Future.microtask(() =>
        context.read<BitcoinProvider>().fetchHistory(limit: _limit));
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final provider = context.watch<BitcoinProvider>();
    final history = provider.historyData;

    return Scaffold(
      appBar: AppBar(
        title: const Text('HISTORICAL CHARTS'),
        actions: [
          PopupMenuButton<int>(
            icon: const Icon(Icons.tune_rounded, color: Color(0xFF00E676)),
            onSelected: (val) {
              setState(() {
                _limit = val;
              });
              provider.fetchHistory(limit: val);
            },
            itemBuilder: (context) => [
              const PopupMenuItem(value: 30, child: Text('Last 30 Days')),
              const PopupMenuItem(value: 100, child: Text('Last 100 Days')),
              const PopupMenuItem(value: 200, child: Text('Last 200 Days')),
            ],
          ),
        ],
      ),
      body: provider.isLoadingHistory
          ? const Center(
              child: CircularProgressIndicator(
                valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF00E676)),
              ),
            )
          : provider.historyError != null
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(30.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.cloud_off_rounded, size: 80, color: Colors.redAccent),
                        const SizedBox(height: 20),
                        Text(
                          'Chart Load Failed',
                          style: theme.textTheme.titleLarge?.copyWith(color: Colors.redAccent),
                        ),
                        const SizedBox(height: 10),
                        Text(
                          provider.historyError!,
                          textAlign: TextAlign.center,
                          style: theme.textTheme.bodyMedium,
                        ),
                        const SizedBox(height: 30),
                        ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFF00E676),
                            foregroundColor: Colors.black,
                            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                          ),
                          onPressed: () => provider.fetchHistory(limit: _limit),
                          icon: const Icon(Icons.refresh_rounded),
                          label: const Text('Retry Connection', style: TextStyle(fontWeight: FontWeight.bold)),
                        ),
                      ],
                    ),
                  ),
                )
              : history.isEmpty
                  ? const Center(child: Text('No historical data available.'))
                  : SingleChildScrollView(
                      child: Padding(
                        padding: const EdgeInsets.all(20.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                            Text(
                              'Bitcoin Historical Price Trend',
                              style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w900),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              'Interactive chart showing the last $_limit trading days close prices.',
                              style: theme.textTheme.bodyMedium,
                            ),
                            const SizedBox(height: 25),

                            // THE CHART CARD
                            CustomCard(
                              padding: const EdgeInsets.fromLTRB(10, 25, 25, 10),
                              child: AspectRatio(
                                aspectRatio: 1.3,
                                child: LineChart(
                                  _buildChartData(history),
                                ),
                              ),
                            ),
                            const SizedBox(height: 25),

                            // QUICK INSIGHT DATA DETAILS
                            _buildInfoStatsCard(theme, history),
                          ],
                        ),
                      ),
                    ),
    );
  }

  LineChartData _buildChartData(List<Map<String, dynamic>> history) {
    List<FlSpot> spots = [];
    double minY = double.infinity;
    double maxY = double.negativeInfinity;

    for (int i = 0; i < history.length; i++) {
      final double close = history[i]['close']?.toDouble() ?? 0.0;
      spots.add(FlSpot(i.toDouble(), close));
      if (close < minY) minY = close;
      if (close > maxY) maxY = close;
    }

    // Add padding to margins
    minY = minY * 0.95;
    maxY = maxY * 1.05;

    return LineChartData(
      gridData: FlGridData(
        show: true,
        drawVerticalLine: true,
        horizontalInterval: (maxY - minY) / 5,
        verticalInterval: history.length / 5,
        getDrawingHorizontalLine: (value) => const FlLine(
          color: Color(0xFF263238),
          strokeWidth: 1,
          dashArray: [5, 5],
        ),
        getDrawingVerticalLine: (value) => const FlLine(
          color: Color(0xFF263238),
          strokeWidth: 1,
          dashArray: [5, 5],
        ),
      ),
      titlesData: FlTitlesData(
        show: true,
        rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        bottomTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            reservedSize: 30,
            interval: history.length / 4,
            getTitlesWidget: (value, meta) {
              int index = value.toInt();
              if (index >= 0 && index < history.length) {
                return SideTitleWidget(
                  axisSide: meta.axisSide,
                  space: 8.0,
                  child: Text(
                    history[index]['date'].substring(5), // returns MM-DD
                    style: const TextStyle(
                      color: Color(0xFF90A4AE),
                      fontWeight: FontWeight.bold,
                      fontSize: 10,
                    ),
                  ),
                );
              }
              return const SizedBox();
            },
          ),
        ),
        leftTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            interval: (maxY - minY) / 4,
            reservedSize: 42,
            getTitlesWidget: (value, meta) {
              return SideTitleWidget(
                axisSide: meta.axisSide,
                space: 6.0,
                child: Text(
                  '\$${(value / 1000).toStringAsFixed(0)}k',
                  style: const TextStyle(
                    color: Color(0xFF90A4AE),
                    fontWeight: FontWeight.bold,
                    fontSize: 10,
                  ),
                ),
              );
            },
          ),
        ),
      ),
      borderData: FlBorderData(
        show: true,
        border: Border.all(color: const Color(0xFF263238), width: 1.5),
      ),
      minX: 0,
      maxX: history.length.toDouble() - 1,
      minY: minY,
      maxY: maxY,
      lineBarsData: [
        LineChartBarData(
          spots: spots,
          isCurved: true,
          gradient: const LinearGradient(
            colors: [Color(0xFF00E676), Color(0xFF00B0FF)],
          ),
          barWidth: 3,
          isStrokeCapRound: true,
          dotData: const FlDotData(show: false),
          belowBarData: BarAreaData(
            show: true,
            gradient: LinearGradient(
              colors: [
                const Color(0xFF00E676).withOpacity(0.2),
                const Color(0xFF00B0FF).withOpacity(0.01),
              ],
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
            ),
          ),
        ),
      ],
      lineTouchData: LineTouchData(
        touchTooltipData: LineTouchTooltipData(
          getTooltipColor: (touchedBarSpot) => const Color(0xFF151B2E),
          tooltipBorder: const BorderSide(color: Color(0xFF00E676), width: 1.0),
          getTooltipItems: (List<LineBarSpot> touchedSpots) {
            return touchedSpots.map((barSpot) {
              final index = barSpot.x.toInt();
              final date = history[index]['date'];
              return LineTooltipItem(
                '\$${barSpot.y.toStringAsFixed(2)}\n$date',
                const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12),
              );
            }).toList();
          },
        ),
      ),
    );
  }

  Widget _buildInfoStatsCard(ThemeData theme, List<Map<String, dynamic>> history) {
    double highest = 0.0;
    double lowest = double.infinity;
    double sum = 0.0;

    for (var day in history) {
      final double close = day['close']?.toDouble() ?? 0.0;
      if (close > highest) highest = close;
      if (close < lowest) lowest = close;
      sum += close;
    }
    double avg = sum / history.length;

    final formatter = NumberFormat.currency(symbol: '\$', decimalDigits: 2);

    return CustomCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '$_limit-Day Analytical Stats',
            style: theme.textTheme.bodyLarge?.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 15),
          _buildStatRow('Highest Close Price', formatter.format(highest), const Color(0xFF00E676)),
          const SizedBox(height: 10),
          _buildStatRow('Lowest Close Price', formatter.format(lowest), const Color(0xFFFF5252)),
          const SizedBox(height: 10),
          _buildStatRow('Average Close Price', formatter.format(avg), const Color(0xFF00B0FF)),
        ],
      ),
    );
  }

  Widget _buildStatRow(String label, String value, Color color) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: const TextStyle(color: Color(0xFF90A4AE), fontSize: 13)),
        Text(
          value,
          style: TextStyle(
            color: color,
            fontWeight: FontWeight.w900,
            fontSize: 14,
          ),
        ),
      ],
    );
  }
}
