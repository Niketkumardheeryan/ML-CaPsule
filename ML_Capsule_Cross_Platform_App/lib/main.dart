import 'package:flutter/material.dart';

void main() {
  runApp(const MlCapsuleApp());
}

class MlCapsuleApp extends StatelessWidget {
  const MlCapsuleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ML-CaPsule',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: const Color(0xFF4F46E5),
        scaffoldBackgroundColor: const Color(0xFFF6F7FB),
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  static const List<_FeatureItem> _features = [
    _FeatureItem(
      icon: Icons.school_outlined,
      title: 'Learn ML Step by Step',
      description:
          'Explore beginner-friendly machine learning projects and examples.',
    ),
    _FeatureItem(
      icon: Icons.psychology_outlined,
      title: 'Deep Learning Resources',
      description:
          'Discover neural networks, NLP, computer vision, and AI projects.',
    ),
    _FeatureItem(
      icon: Icons.dataset_outlined,
      title: 'Project-Based Practice',
      description:
          'Use real-world datasets and notebooks to strengthen practical skills.',
    ),
    _FeatureItem(
      icon: Icons.rocket_launch_outlined,
      title: 'Open Source Learning',
      description: 'Contribute, learn, and grow with the ML-CaPsule community.',
    ),
  ];

  static const List<String> topics = [
    'Machine Learning',
    'Deep Learning',
    'NLP',
    'Computer Vision',
    'Data Analysis',
    'Statistics',
    'Model Deployment',
    'Visualization',
  ];

  static const List<String> projects = [
    'Diabetes Prediction',
    'Fake News Detection',
    'Customer Segmentation',
    'Brain Tumor Detection',
    'Handwritten Digit Recognition',
    'Stock Price Analysis',
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ML-CaPsule'),
        centerTitle: true,
        backgroundColor: Colors.transparent,
      ),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            const _HeroCard(),
            const SizedBox(height: 18),
            const _InfoStats(),
            const SizedBox(height: 26),
            const _SectionTitle('Explore ML-CaPsule'),
            const SizedBox(height: 12),
            ..._features.map((feature) => _FeatureCard(feature: feature)),
            const SizedBox(height: 24),
            const _SectionTitle('Topics Covered'),
            const SizedBox(height: 12),
            Wrap(
              spacing: 10,
              runSpacing: 10,
              children: topics
                  .map((topic) => _TopicChip(label: topic))
                  .toList(),
            ),
            const SizedBox(height: 24),
            const _SectionTitle('Sample Projects'),
            const SizedBox(height: 12),
            ...projects.map((project) => _ProjectTile(title: project)),
            const SizedBox(height: 24),
            const _FooterCard(),
          ],
        ),
      ),
    );
  }
}

class _HeroCard extends StatelessWidget {
  const _HeroCard();

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(28),
        gradient: const LinearGradient(
          colors: [Color(0xFF4F46E5), Color(0xFF7C3AED)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        boxShadow: const [
          BoxShadow(
            color: Color(0x26000000),
            blurRadius: 18,
            offset: Offset(0, 10),
          ),
        ],
      ),
      child: const Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(Icons.auto_graph_rounded, color: Colors.white, size: 46),
          SizedBox(height: 18),
          Text(
            'Machine Learning from Basic to Advance',
            style: TextStyle(
              color: Colors.white,
              fontSize: 27,
              fontWeight: FontWeight.w800,
              height: 1.12,
            ),
          ),
          SizedBox(height: 12),
          Text(
            'A compact cross-platform mobile app for exploring ML-CaPsule projects, topics, and learning resources.',
            style: TextStyle(
              color: Color(0xFFEDE9FE),
              fontSize: 15.5,
              height: 1.45,
            ),
          ),
        ],
      ),
    );
  }
}

class _InfoStats extends StatelessWidget {
  const _InfoStats();

  @override
  Widget build(BuildContext context) {
    return const Row(
      children: [
        Expanded(
          child: _StatCard(value: 'ML', label: 'Projects'),
        ),
        SizedBox(width: 10),
        Expanded(
          child: _StatCard(value: 'AI', label: 'Learning'),
        ),
        SizedBox(width: 10),
        Expanded(
          child: _StatCard(value: 'OSS', label: 'Community'),
        ),
      ],
    );
  }
}

class _StatCard extends StatelessWidget {
  final String value;
  final String label;

  const _StatCard({required this.value, required this.label});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 17),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(22),
        border: Border.all(color: const Color(0x11000000)),
      ),
      child: Column(
        children: [
          Text(
            value,
            style: const TextStyle(fontSize: 21, fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 4),
          Text(label, style: const TextStyle(color: Color(0xFF6B7280))),
        ],
      ),
    );
  }
}

class _SectionTitle extends StatelessWidget {
  final String title;

  const _SectionTitle(this.title);

  @override
  Widget build(BuildContext context) {
    return Text(
      title,
      style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800),
    );
  }
}

class _FeatureCard extends StatelessWidget {
  final _FeatureItem feature;

  const _FeatureCard({required this.feature});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(22),
        border: Border.all(color: const Color(0x11000000)),
      ),
      child: Row(
        children: [
          CircleAvatar(
            radius: 24,
            backgroundColor: const Color(0xFFEDE9FE),
            child: Icon(feature.icon, color: const Color(0xFF4F46E5)),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  feature.title,
                  style: const TextStyle(
                    fontSize: 15.5,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  feature.description,
                  style: const TextStyle(
                    color: Color(0xFF6B7280),
                    height: 1.35,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _TopicChip extends StatelessWidget {
  final String label;

  const _TopicChip({required this.label});

  @override
  Widget build(BuildContext context) {
    return Chip(
      label: Text(label),
      backgroundColor: Colors.white,
      side: const BorderSide(color: Color(0x11000000)),
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
    );
  }
}

class _ProjectTile extends StatelessWidget {
  final String title;

  const _ProjectTile({required this.title});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 0,
      color: Colors.white,
      margin: const EdgeInsets.only(bottom: 10),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
      child: ListTile(
        leading: const Icon(
          Icons.folder_copy_outlined,
          color: Color(0xFF4F46E5),
        ),
        title: Text(title),
        subtitle: const Text('Explore project resources in the repository'),
        trailing: const Icon(Icons.chevron_right_rounded),
      ),
    );
  }
}

class _FooterCard extends StatelessWidget {
  const _FooterCard();

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: const Color(0xFF111827),
        borderRadius: BorderRadius.circular(24),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Start exploring ML-CaPsule',
            style: TextStyle(
              color: Colors.white,
              fontSize: 19,
              fontWeight: FontWeight.w800,
            ),
          ),
          const SizedBox(height: 8),
          const Text(
            'This app gives a mobile-first overview of ML-CaPsule and its project-based learning approach.',
            style: TextStyle(color: Color(0xFFD1D5DB), height: 1.4),
          ),
          const SizedBox(height: 14),
          FilledButton.icon(
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text(
                    'Repository link support can be added in the next update.',
                  ),
                ),
              );
            },
            icon: const Icon(Icons.open_in_new_rounded),
            label: const Text('Explore Repository'),
          ),
        ],
      ),
    );
  }
}

class _FeatureItem {
  final IconData icon;
  final String title;
  final String description;

  const _FeatureItem({
    required this.icon,
    required this.title,
    required this.description,
  });
}
