import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class BitcoinProvider extends ChangeNotifier {
  // Replace with local IP or server URL for physical device/emulator testing
  // 10.0.2.2 is the standard loopback IP for Android Emulator pointing to localhost
  final String _baseUrl = 'http://10.0.2.2:8000';

  Map<String, dynamic>? _marketOverview;
  List<Map<String, dynamic>> _historyData = [];
  Map<String, dynamic>? _predictionResult;

  bool _isLoadingOverview = false;
  bool _isLoadingHistory = false;
  bool _isPredicting = false;

  String? _overviewError;
  String? _historyError;
  String? _predictionError;

  // Getters
  Map<String, dynamic>? get marketOverview => _marketOverview;
  List<Map<String, dynamic>> get historyData => _historyData;
  Map<String, dynamic>? get predictionResult => _predictionResult;

  bool get isLoadingOverview => _isLoadingOverview;
  bool get isLoadingHistory => _isLoadingHistory;
  bool get isPredicting => _isPredicting;

  String? get overviewError => _overviewError;
  String? get historyError => _historyError;
  String? get predictionError => _predictionError;

  // Fetch Market Summary
  Future<void> fetchMarketOverview() async {
    _isLoadingOverview = true;
    _overviewError = null;
    notifyListeners();

    try {
      final response = await http.get(Uri.parse('$_baseUrl/market-overview'));
      if (response.statusCode == 200) {
        _marketOverview = jsonDecode(response.body);
      } else {
        _overviewError = 'Failed to load market overview: ${response.statusCode}';
      }
    } catch (e) {
      _overviewError = 'Server is offline. Start the backend app first.';
    } finally {
      _isLoadingOverview = false;
      notifyListeners();
    }
  }

  // Fetch Historical prices for chart
  Future<void> fetchHistory({int limit = 100}) async {
    _isLoadingHistory = true;
    _historyError = null;
    notifyListeners();

    try {
      final response = await http.get(Uri.parse('$_baseUrl/history?limit=$limit'));
      if (response.statusCode == 200) {
        final decoded = jsonDecode(response.body);
        _historyData = List<Map<String, dynamic>>.from(decoded['data']);
      } else {
        _historyError = 'Failed to load history: ${response.statusCode}';
      }
    } catch (e) {
      _historyError = 'Could not establish connection to server.';
    } finally {
      _isLoadingHistory = false;
      notifyListeners();
    }
  }

  // Predict Close price and Marketcap
  Future<bool> makePrediction({
    required double high,
    required double low,
    required double openPrice,
    required double volume,
  }) async {
    _isPredicting = true;
    _predictionError = null;
    _predictionResult = null;
    notifyListeners();

    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/predict'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'high': high,
          'low': low,
          'open_price': openPrice,
          'volume': volume,
        }),
      );

      if (response.statusCode == 200) {
        _predictionResult = jsonDecode(response.body);
        notifyListeners();
        return true;
      } else {
        final decoded = jsonDecode(response.body);
        _predictionError = decoded['detail'] ?? 'Failed to perform prediction.';
        return false;
      }
    } catch (e) {
      _predictionError = 'Cannot communicate with prediction server.';
      return false;
    } finally {
      _isPredicting = false;
      notifyListeners();
    }
  }

  // Helper to trigger all core data updates
  Future<void> refreshAll() async {
    await Future.wait([
      fetchMarketOverview(),
      fetchHistory(),
    ]);
  }
}
