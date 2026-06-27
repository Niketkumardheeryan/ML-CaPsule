import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/bitcoin_provider.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => BitcoinProvider()..refreshAll(),
      child: MaterialApp(
        title: 'Bitcoin Price Predictor',
        debugShowCheckedModeBanner: false,
        themeMode: ThemeMode.dark,
        darkTheme: ThemeData(
          useMaterial3: true,
          brightness: Brightness.dark,
          scaffoldBackgroundColor: const Color(0xFF0A0E1A), // Sleek deep space black
          primaryColor: const Color(0xFF00E676), // Neon Green accent
          colorScheme: const ColorScheme.dark(
            primary: Color(0xFF00E676), // Neon Green
            secondary: Color(0xFF00B0FF), // Cyber Blue
            surface: Color(0xFF151B2E), // Premium dark card color
            background: Color(0xFF0A0E1A),
            error: Color(0xFFFF5252),
          ),
          cardTheme: CardTheme(
            color: const Color(0xFF151B2E),
            elevation: 8,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(20),
            ),
          ),
          textTheme: const TextTheme(
            headlineMedium: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: Colors.white,
              letterSpacing: 0.5,
            ),
            titleLarge: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
            bodyLarge: TextStyle(
              fontSize: 16,
              color: Color(0xFF90A4AE),
            ),
            bodyMedium: TextStyle(
              fontSize: 14,
              color: Color(0xFF90A4AE),
            ),
          ),
          appBarTheme: const AppBarTheme(
            backgroundColor: Color(0xFF0A0E1A),
            elevation: 0,
            centerTitle: true,
            titleTextStyle: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.w900,
              color: Colors.white,
              letterSpacing: 1.0,
            ),
            iconTheme: IconThemeData(color: Colors.white),
          ),
          inputDecorationTheme: InputDecorationTheme(
            filled: true,
            fillColor: const Color(0xFF1C243B),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(15),
              borderSide: BorderSide.none,
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(15),
              borderSide: const BorderSide(color: Color(0xFF00E676), width: 1.5),
            ),
            labelStyle: const TextStyle(color: Color(0xFF90A4AE)),
            floatingLabelStyle: const TextStyle(color: Color(0xFF00E676)),
            hintStyle: const TextStyle(color: Color(0xFF546E7A)),
          ),
        ),
        home: const HomeScreen(),
      ),
    );
  }
}
