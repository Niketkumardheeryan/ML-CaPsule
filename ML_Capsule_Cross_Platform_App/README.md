# ML-CaPsule Cross Platform App

A basic cross-platform mobile application for the ML-CaPsule repository.

This app gives users a mobile-first overview of ML-CaPsule, its learning approach, major machine learning topics, and sample project areas.

## Features

- Cross-platform Flutter app structure for Android and iOS
- Clean ML-CaPsule landing screen
- Overview section for project-based learning
- Topic chips for Machine Learning, Deep Learning, NLP, Computer Vision, Data Analysis, Statistics, Model Deployment, and Visualization
- Sample project list
- Material 3 based responsive UI
- Widget test coverage
- Android release APK included

## Tech Stack

- Flutter
- Dart
- Material 3

## Folder Structure

```text
ML_Capsule_Cross_Platform_App/
|-- android/
|-- ios/
|-- lib/
|   |-- main.dart
|-- test/
|   |-- widget_test.dart
|-- release/
|   |-- ml_capsule_app_v1.apk
|-- pubspec.yaml
|-- README.md
```

## Getting Started

### Prerequisites

Install Flutter and Android Studio.

Check Flutter setup:

```bash
flutter doctor
```

### Install Dependencies

```bash
flutter pub get
```

### Run the App

```bash
flutter run
```

### Run Static Analysis

```bash
flutter analyze
```

### Run Tests

```bash
flutter test
```

### Build Android APK

```bash
flutter build apk --release
```

The generated APK is included at:

```text
release/ml_capsule_app_v1.apk
```

## iOS Note

The iOS project structure is included under the `ios/` directory. Building and archiving the iOS app requires macOS with Xcode.

## Local Verification

The following checks were run successfully:

```bash
dart format lib/main.dart test/widget_test.dart
flutter analyze
flutter test
flutter build apk --release
```

## Related Issue

Fixes #1905
