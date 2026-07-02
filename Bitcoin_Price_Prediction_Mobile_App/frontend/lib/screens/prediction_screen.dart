import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../providers/bitcoin_provider.dart';
import '../widgets/custom_card.dart';

class PredictionScreen extends StatefulWidget {
  const PredictionScreen({super.key});

  @override
  State<PredictionScreen> createState() => _PredictionScreenState();
}

class _PredictionScreenState extends State<PredictionScreen> {
  final _formKey = GlobalKey<FormState>();
  final _highController = TextEditingController();
  final _lowController = TextEditingController();
  final _openController = TextEditingController();
  final _volumeController = TextEditingController();

  @override
  void dispose() {
    _highController.dispose();
    _lowController.dispose();
    _openController.dispose();
    _volumeController.dispose();
    super.dispose();
  }

  String _formatCurrency(dynamic value) {
    if (value == null) return '\$0.00';
    final formatter = NumberFormat.currency(symbol: '\$', decimalDigits: 2);
    return formatter.format(value);
  }

  void _submit() async {
    if (_formKey.currentState!.validate()) {
      final high = double.parse(_highController.text.trim());
      final low = double.parse(_lowController.text.trim());
      final open = double.parse(_openController.text.trim());
      final volume = double.parse(_volumeController.text.trim());

      final success = await context.read<BitcoinProvider>().makePrediction(
            high: high,
            low: low,
            openPrice: open,
            volume: volume,
          );

      if (success && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Bitcoin prediction loaded successfully!'),
            backgroundColor: Color(0xFF00E676),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final provider = context.watch<BitcoinProvider>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('ML PREDICTOR'),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // HEADER INTRO
              Text(
                'Intraday ML Predictor',
                style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w900),
              ),
              const SizedBox(height: 8),
              Text(
                'Enter high, low, opening price and trading volume to predict the closing price and market cap.',
                style: theme.textTheme.bodyMedium,
              ),
              const SizedBox(height: 25),

              // THE FORM
              Form(
                key: _formKey,
                child: Column(
                  children: [
                    _buildTextField(
                      controller: _openController,
                      label: 'Opening Price (USD)',
                      hint: 'e.g. 58340.50',
                      icon: Icons.login_rounded,
                    ),
                    const SizedBox(height: 15),
                    Row(
                      children: [
                        Expanded(
                          child: _buildTextField(
                            controller: _highController,
                            label: 'Intraday High',
                            hint: 'e.g. 59200.00',
                            icon: Icons.arrow_upward_rounded,
                          ),
                        ),
                        const SizedBox(width: 15),
                        Expanded(
                          child: _buildTextField(
                            controller: _lowController,
                            label: 'Intraday Low',
                            hint: 'e.g. 57450.00',
                            icon: Icons.arrow_downward_rounded,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 15),
                    _buildTextField(
                      controller: _volumeController,
                      label: 'Trading Volume (USD)',
                      hint: 'e.g. 34500000000',
                      icon: Icons.bar_chart_rounded,
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 30),

              // SUBMIT BUTTON OR LOADING INDICATOR
              provider.isPredicting
                  ? const Center(
                      child: CircularProgressIndicator(
                        valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF00E676)),
                      ),
                    )
                  : ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF00E676),
                        foregroundColor: Colors.black,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(15),
                        ),
                      ),
                      onPressed: _submit,
                      child: const Text(
                        'CALCULATE PREDICTION',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          letterSpacing: 1.0,
                        ),
                      ),
                    ),
              const SizedBox(height: 30),

              // ERROR MESSAGE IF PRESENT
              if (provider.predictionError != null)
                Container(
                  padding: const EdgeInsets.all(15),
                  decoration: BoxDecoration(
                    color: Colors.redAccent.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(15),
                    border: Border.all(color: Colors.redAccent.withOpacity(0.5)),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.error_outline_rounded, color: Colors.redAccent),
                      const SizedBox(width: 15),
                      Expanded(
                        child: Text(
                          provider.predictionError!,
                          style: const TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ],
                  ),
                ),

              // PREDICTION RESULTS DASHBOARD CARD
              if (provider.predictionResult != null) ...[
                Text(
                  'ML Prediction Results',
                  style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w900),
                ),
                const SizedBox(height: 15),
                _buildResultsCard(theme, provider.predictionResult!, double.parse(_openController.text)),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required String label,
    required String hint,
    required IconData icon,
  }) {
    return TextFormField(
      controller: controller,
      keyboardType: const TextInputType.numberWithOptions(decimal: true),
      style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
      decoration: InputDecoration(
        labelText: label,
        hintText: hint,
        prefixIcon: Icon(icon, color: Colors.grey[500]),
      ),
      validator: (value) {
        if (value == null || value.trim().isEmpty) {
          return 'This field is required';
        }
        if (double.tryParse(value.trim()) == null) {
          return 'Enter a valid numeric value';
        }
        if (double.parse(value.trim()) <= 0) {
          return 'Value must be greater than 0';
        }
        return null;
      },
    );
  }

  Widget _buildResultsCard(ThemeData theme, Map<String, dynamic> result, double openPrice) {
    final double predClose = result['predicted_close'] ?? 0.0;
    final double predMc = result['predicted_marketcap'] ?? 0.0;
    final double diff = predClose - openPrice;
    final bool isUp = diff >= 0;
    final String diffSign = isUp ? '+' : '';
    final Color diffColor = isUp ? const Color(0xFF00E676) : const Color(0xFFFF5252);
    final String trendLabel = isUp ? 'Bullish Closing Prediction 📈' : 'Bearish Closing Prediction 📉';

    return CustomCard(
      borderColor: diffColor.withOpacity(0.4),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Predicted Close Price',
                style: theme.textTheme.bodyMedium?.copyWith(color: Colors.grey[400], fontWeight: FontWeight.bold),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: diffColor.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  isUp ? 'GAIN' : 'LOSS',
                  style: TextStyle(color: diffColor, fontSize: 11, fontWeight: FontWeight.w900),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            _formatCurrency(predClose),
            style: theme.textTheme.headlineMedium?.copyWith(
              fontSize: 32,
              fontWeight: FontWeight.w900,
              color: Colors.white,
            ),
          ),
          const SizedBox(height: 10),
          Row(
            children: [
              Text(
                'Net Change: ',
                style: theme.textTheme.bodyMedium?.copyWith(color: Colors.grey[500]),
              ),
              Text(
                '$diffSign${_formatCurrency(diff)}',
                style: theme.textTheme.bodyMedium?.copyWith(color: diffColor, fontWeight: FontWeight.w900),
              ),
            ],
          ),
          const SizedBox(height: 15),
          const Divider(color: Color(0xFF263238), thickness: 1.5),
          const SizedBox(height: 15),
          Text(
            'Predicted Marketcap',
            style: theme.textTheme.bodyMedium?.copyWith(color: Colors.grey[400], fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          Text(
            _formatCurrency(predMc),
            style: theme.textTheme.titleLarge?.copyWith(
              fontSize: 22,
              fontWeight: FontWeight.bold,
              color: const Color(0xFF00B0FF),
            ),
          ),
          const SizedBox(height: 20),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: const Color(0xFF0A0E1A),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Text(
              trendLabel,
              textAlign: TextAlign.center,
              style: TextStyle(
                color: diffColor,
                fontWeight: FontWeight.bold,
                fontSize: 13,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
