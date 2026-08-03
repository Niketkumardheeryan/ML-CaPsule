import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../providers/bitcoin_provider.dart';
import '../widgets/custom_card.dart';
import 'prediction_screen.dart';
import 'chart_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  String _formatCurrency(dynamic value) {
    if (value == null) return '\$0.00';
    final formatter = NumberFormat.currency(symbol: '\$', decimalDigits: 2);
    return formatter.format(value);
  }

  String _formatVolume(dynamic value) {
    if (value == null) return '0';
    final formatter = NumberFormat.compactCurrency(symbol: '');
    return formatter.format(value);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('BTC PREDICTOR'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh_rounded, color: Color(0xFF00E676)),
            onPressed: () {
              context.read<BitcoinProvider>().refreshAll();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('Updating live Bitcoin data...'),
                  backgroundColor: Color(0xFF151B2E),
                ),
              );
            },
          ),
        ],
      ),
      body: Consumer<BitcoinProvider>(
        builder: (context, provider, child) {
          if (provider.isLoadingOverview) {
            return const Center(
              child: CircularProgressIndicator(
                valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF00E676)),
              ),
            );
          }

          if (provider.overviewError != null) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(30.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.cloud_off_rounded, size: 80, color: Colors.redAccent),
                    const SizedBox(height: 20),
                    Text(
                      'Connection Issue',
                      style: theme.textTheme.titleLarge?.copyWith(color: Colors.redAccent),
                    ),
                    const SizedBox(height: 10),
                    Text(
                      provider.overviewError!,
                      textAlign: Center,
                      style: theme.textTheme.bodyMedium,
                    ),
                    const SizedBox(height: 30),
                    ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF00E676),
                        foregroundColor: Colors.black,
                        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(15),
                        ),
                      ),
                      onPressed: () => provider.refreshAll(),
                      icon: const Icon(Icons.refresh_rounded),
                      label: const Text('Try Again', style: TextStyle(fontWeight: FontWeight.bold)),
                    ),
                  ],
                ),
              ),
            );
          }

          final overview = provider.marketOverview;
          if (overview == null) {
            return const Center(child: Text('No data loaded.'));
          }

          final bool isBullish = overview['market_trend']?.toString().contains('Bullish') ?? true;
          final trendColor = isBullish ? const Color(0xFF00E676) : const Color(0xFFFF5252);

          return RefreshIndicator(
            color: const Color(0xFF00E676),
            backgroundColor: const Color(0xFF151B2E),
            onRefresh: () => provider.refreshAll(),
            child: SingleChildScrollView(
              physics: const AlwaysScrollableScrollPhysics(),
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // HERO CARD: Current Bitcoin Price & Trend
                    CustomCard(
                      borderColor: trendColor.withOpacity(0.4),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                'Bitcoin Price (BTC)',
                                style: theme.textTheme.bodyLarge?.copyWith(
                                  fontWeight: FontWeight.bold,
                                  color: Colors.grey[400],
                                ),
                              ),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                decoration: BoxDecoration(
                                  color: trendColor.withOpacity(0.15),
                                  borderRadius: BorderRadius.circular(20),
                                ),
                                child: Text(
                                  overview['market_trend'] ?? 'Stable',
                                  style: TextStyle(
                                    color: trendColor,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 12,
                                  ),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 12),
                          Text(
                            _formatCurrency(overview['latest_price']),
                            style: theme.textTheme.headlineMedium?.copyWith(
                              fontSize: 36,
                              letterSpacing: -0.5,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Last updated: ${overview['latest_date']}',
                            style: theme.textTheme.bodyMedium?.copyWith(color: Colors.grey[500]),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 25),

                    // SECTION TITLE: Insights
                    Text(
                      'Market Insights',
                      style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800),
                    ),
                    const SizedBox(height: 15),

                    // GRID OF CARDS: Market Insights
                    GridView.count(
                      crossAxisCount: 2,
                      crossAxisSpacing: 15,
                      mainAxisSpacing: 15,
                      shrinkWrap: true,
                      childAspectRatio: 1.3,
                      physics: const NeverScrollableScrollPhysics(),
                      children: [
                        _buildStatCard(
                          context,
                          'All-Time High',
                          _formatCurrency(overview['all_time_high']),
                          Icons.trending_up_rounded,
                          const Color(0xFF00E676),
                        ),
                        _buildStatCard(
                          context,
                          'All-Time Low',
                          _formatCurrency(overview['all_time_low']),
                          Icons.trending_down_rounded,
                          const Color(0xFFFF5252),
                        ),
                        _buildStatCard(
                          context,
                          'Avg Volume (20d)',
                          _formatVolume(overview['average_volume_20d']),
                          Icons.bar_chart_rounded,
                          const Color(0xFF00B0FF),
                        ),
                        _buildStatCard(
                          context,
                          'Recommendation',
                          overview['recommendation'] ?? 'Hold',
                          Icons.lightbulb_rounded,
                          const Color(0xFFFFD700),
                        ),
                      ],
                    ),
                    const SizedBox(height: 25),

                    // MINI CHART CARD PREVIEW
                    CustomCard(
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (_) => const ChartScreen()),
                        );
                      },
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Historical Prices',
                                style: theme.textTheme.bodyLarge?.copyWith(fontWeight: FontWeight.bold),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                'Tap to view interactive Bitcoin charts',
                                style: theme.textTheme.bodyMedium?.copyWith(color: Colors.grey[500]),
                              ),
                            ],
                          ),
                          const Icon(
                            Icons.show_chart_rounded,
                            size: 32,
                            color: Color(0xFF00E676),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 30),

                    // BUTTON CARD: Predict Tomorrow's Price
                    CustomCard(
                      borderColor: const Color(0xFF00B0FF).withOpacity(0.4),
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (_) => const PredictionScreen()),
                        );
                      },
                      child: Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: const Color(0xFF00B0FF).withOpacity(0.15),
                              borderRadius: BorderRadius.circular(15),
                            ),
                            child: const Icon(
                              Icons.psychology_rounded,
                              color: Color(0xFF00B0FF),
                              size: 36,
                            ),
                          ),
                          const SizedBox(width: 20),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'AI Price Prediction',
                                  style: theme.textTheme.bodyLarge?.copyWith(
                                    fontWeight: FontWeight.w900,
                                    color: Colors.white,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  'Estimate Close Price & Marketcap with ML',
                                  style: theme.textTheme.bodyMedium?.copyWith(color: Colors.grey[400]),
                                ),
                              ],
                            ),
                          ),
                          const Icon(Icons.arrow_forward_ios_rounded, size: 16, color: Color(0xFF00B0FF)),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildStatCard(
    BuildContext context,
    String label,
    String value,
    IconData icon,
    Color color,
  ) {
    final theme = Theme.of(context);
    return CustomCard(
      padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 12.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                label,
                style: theme.textTheme.bodyMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: Colors.grey[500],
                  fontSize: 12,
                ),
              ),
              Icon(icon, color: color.withOpacity(0.8), size: 20),
            ],
          ),
          Text(
            value,
            style: theme.textTheme.bodyLarge?.copyWith(
              fontSize: 16,
              fontWeight: FontWeight.w900,
              color: Colors.white,
            ),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }
}
