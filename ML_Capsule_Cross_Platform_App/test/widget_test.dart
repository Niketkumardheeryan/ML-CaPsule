import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ml_capsule_app/main.dart';

void main() {
  testWidgets('renders ML-CaPsule home screen content', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(const MlCapsuleApp());

    expect(find.text('ML-CaPsule'), findsWidgets);
    expect(find.text('Machine Learning from Basic to Advance'), findsOneWidget);
    expect(find.text('Explore ML-CaPsule'), findsOneWidget);
    expect(find.byIcon(Icons.auto_graph_rounded), findsOneWidget);

    await tester.scrollUntilVisible(
      find.text('Topics Covered'),
      300,
      scrollable: find.byType(Scrollable),
    );

    expect(find.text('Topics Covered'), findsOneWidget);
    expect(find.text('Machine Learning'), findsWidgets);
  });
}
