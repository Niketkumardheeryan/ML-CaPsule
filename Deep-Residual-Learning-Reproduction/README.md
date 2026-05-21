# Deep Residual Learning — Reproduction Study

> Reproducing the degradation problem and residual learning fix from:  
> **He et al., "Deep Residual Learning for Image Recognition" (CVPR 2016)**

---

## 1. Problem — The Degradation Problem

A well-established intuition in deep learning is: *deeper networks should perform better*.  
A deeper model always has at least the same representational capacity as a shallower one — in theory, extra layers can simply learn identity mappings and add no harm.

**In practice, this breaks down.**

The original paper observed that on CIFAR-10:
- A **56-layer plain CNN** performs *worse* than a **20-layer plain CNN** — even on training data.

This is not overfitting. The training error itself is higher for the deeper model.

**Root cause — two compounding mechanisms:**
1. **Optimization difficulty:** Plain CNNs cannot learn identity mappings. Each layer distorts the signal. Across many layers, these distortions compound.
2. **Vanishing gradients:** Gradient signal shrinks multiplicatively through every weight matrix. Early layers receive near-zero updates and stop learning.

> ⚠️ The paper explicitly states degradation is **not** solely a vanishing gradient problem. Both mechanisms contribute.

---

## 2. Hypothesis

> Reformulating the learning objective as a residual reduces optimization difficulty and enables deeper networks to train effectively.

Instead of learning:
```
H(x)          ← full transformation (hard)
```

Learn:
```
F(x) = H(x) - x     ← residual (difference from identity)
Output = F(x) + x
```

**If identity is optimal:** the network only needs to push F(x) → 0.  
Weights go to zero — trivially easy.  
In a plain CNN, learning H(x) = x requires precise weight configuration with no inherent bias toward identity.

---

## 3. Method — Comparative Experiment

**Dataset:** CIFAR-10 (50k train / 10k test, 10 classes)

**Models:**

| Model     | Architecture | Depth | Skip Connection | Channels      | Params  |
|-----------|-------------|-------|-----------------|---------------|---------|
| CNN-20    | Plain CNN   | 20    | ✗               | 16 (constant) | 45,210  |
| CNN-56    | Plain CNN   | 56    | ✗               | 16 (constant) | 120,346 |
| ResNet-20 | ResNet      | 20    | ✓               | 16→32→64      | 272,474 |
| ResNet-32 | ResNet      | 32    | ✓               | 16→32→64      | 466,906 |

> **Why CNN-56 instead of CNN-32?** A larger depth gap produces a clearer degradation signal. CNN-20 vs CNN-32 is noisy with BatchNorm stabilizing training. CNN-56 matches the paper's original comparison.

**Training setup (identical for all models):**
- Optimizer: SGD (momentum=0.9, weight_decay=1e-4)
- Learning rate: 0.1
- Batch size: 128
- Epochs: 50
- Random seed: 42

### ⚠️ What This Experiment Can and Cannot Claim

This is a **comparative experiment**, not a perfectly controlled one. CNN and ResNet differ in more than skip connections:

| Difference | CNN | ResNet |
|---|---|---|
| Skip connection | ✗ | ✓ |
| Channel width | 16 constant | 16 → 32 → 64 |
| Parameter count | ~45K (depth-20) | ~272K (depth-20) |
| Feature hierarchy | flat | staged |

**Two separate claims — with different levels of rigor:**

**Claim 1 — Degradation exists (strong, self-contained):**  
CNN-56 performs worse than CNN-20 despite having more parameters. The CNN family alone proves this — no ResNet comparison needed. Capacity cannot explain it; more parameters made performance worse.

**Claim 2 — Residual learning helps (directional, not fully isolated):**  
ResNet-32 outperforms ResNet-20. Depth helps residual networks. The CNN vs ResNet gap is directional evidence — channel width, capacity, and architecture style also differ, so skip connections cannot be isolated as the sole cause.

---

## 4. Results

### 4.1 Training Dynamics

> 📊 **[INSERT: training loss curve plot — CNN-20 vs CNN-56 vs ResNet-20 vs ResNet-32]**

CNN-56 maintains higher training loss than CNN-20 throughout training — including on the training set itself — indicating optimization failure rather than overfitting, since the gap persists where overfitting would not. ResNet-32 converges to lower loss than ResNet-20, demonstrating that depth benefits residual networks.

---

### 4.2 Test Accuracy — Phase 1

| Model     | Accuracy (%) |
|-----------|-------------|
| CNN-20    | 73.64        |
| CNN-56    | 53.23        |
| ResNet-20 | 78.50        |
| ResNet-32 | 81.70        |

CNN-56 underperforms CNN-20 by **−20.41%** despite having more parameters. ResNet-32 outperforms ResNet-20 by **+3.20%**. Architectural design — not parameter count — determines whether depth helps or hurts.

---

### 4.3 Engineering Improvements — Phase 2

| Model     | Phase 1 (%) | Phase 2 (%) | Δ       |
|-----------|------------|------------|---------|
| CNN-20    | 73.64      | 82.06      | +8.42   |
| CNN-56    | 53.23      | 58.94      | +5.71   |
| ResNet-20 | 78.50      | 89.33      | +10.83  |
| ResNet-32 | 81.70      | 90.01      | +8.31   |

Augmentation and LR scheduling improve accuracy across all models. However, **CNN-56 continues to underperform CNN-20 even after improvements** (58.94% vs 82.06% — a gap of −23.12%). Training strategy cannot compensate for optimization failure caused by depth in plain CNNs.

> **Scope note:** Only augmentation and LR scheduling were tested. The claim is limited to these specific training strategies.

---

### 4.4 Final Verdict

```
Degradation (Phase 1): CNN-56 vs CNN-20      = −20.41%  ← CONFIRMED
Degradation (Phase 2): CNN-56 vs CNN-20      = −23.12%  ← still there after improvements
Residual fix:          ResNet-32 vs ResNet-20 = +3.20%   ← depth helps residual models
```

**Conclusion:**
- Plain CNNs degrade with depth: optimization failure, not overfitting
- One change — adding F(x) + x — resolves this
- Training improvements help all models but cannot fix the architecture
- Architecture, not training strategy, determines optimization scalability

---

## 5. Why It Works — Optimization Mechanism

**Two mechanisms — not one:**

**Mechanism 1 — Easier identity mapping:**  
Residual learning changes what must be learned. Instead of H(x) = x (hard), the network learns F(x) = 0 (trivial — weights go to zero). This directly addresses optimization difficulty at depth.

**Mechanism 2 — Improved gradient flow:**  
During backprop, `output = F(x) + x` yields:

```
∂L/∂x  =  ∂L/∂out · (∂F(x)/∂x  +  1)
                                    ↑
                           identity term — always present
```

Even when `∂F(x)/∂x` shrinks to near-zero, the `+1` ensures gradient reaches earlier layers. Plain CNNs have no such path — gradients shrink multiplicatively across every layer.

---

## 6. Trade-off Analysis

| Model     | Params  | Phase 1 Acc | Phase 2 Acc |
|-----------|---------|------------|------------|
| CNN-20    | 45,210  | 73.64%     | 82.06%     |
| CNN-56    | 120,346 | 53.23%     | 58.94%     |
| ResNet-20 | 272,474 | 78.50%     | 89.33%     |
| ResNet-32 | 466,906 | 81.70%     | 90.01%     |

<!-- FILL IN: time/epoch from your training output -->

CNN-56 has more parameters than CNN-20 yet performs worse — demonstrating that parameter count alone does not predict performance. ResNet-20 offers the best accuracy-efficiency trade-off for deployment.

---

## 7. Known Limitations

| Limitation | Impact |
|---|---|
| CNN vs ResNet differ in channels + params, not just skip connections | Cannot claim skip connection is the *sole* cause of CNN vs ResNet gap |
| BatchNorm in CNN baseline | BN stabilizes training; real degradation likely worse without it |
| CIFAR-10 is relatively easy | Degradation signal weaker than on harder datasets |
| Single run, no variance | Results may vary ±2–5% across seeds |

**The two core claims this experiment supports:**
- ✅ **Claim 1 (strong):** CNN-56 < CNN-20 on training data despite more params → degradation is real
- ✅ **Claim 2 (directional):** ResNet-32 > ResNet-20 → residual learning scales with depth

---

## 8. Implementation Notes

- **Degradation needs sufficient epochs:** Effect not clearly visible until 40–50 epochs. Optimization failure accumulates over training, not immediately.
- **Architecture comparability:** CNN and ResNet cannot be made structurally identical while preserving ResNet's staged design. Parameter mismatch documented as limitation, not silently ignored.
- **Projection shortcut:** Stride=2 stage transitions require 1×1 conv to match dimensions. Missing this causes shape mismatch errors easily confused with a training bug.

---

## 🔬 Key Takeaway

> **Architectural design, not training strategy, determines optimization success in deep networks.**  
> CNN-56 has more parameters than CNN-20 — and performs worse. This single fact destroys the argument that deeper models fail because they have insufficient capacity. The problem is optimization, not representation.  
> One line — `out = F(x) + x` — resolves it.

---

## ❓ Interview Questions — Prepared Answers

**Q: Why does CNN-56 having more parameters but worse accuracy prove it's an optimization problem?**  
If the problem were capacity, more parameters would help. They didn't — they made things worse. The only remaining explanation is that the network has the capacity but cannot *learn* to use it correctly at depth. That is optimization failure by definition.

**Q: Why does "worse on training data" prove it's not overfitting?**  
Overfitting means: good training accuracy, bad test accuracy. Here, training accuracy is also worse. The model is failing to minimize its own training objective. That is not overfitting — it is optimization failure.

**Q: Why doesn't augmentation fix CNN-56?**  
Augmentation helps generalization. Degradation is an optimization failure — the model cannot minimize *training* loss. Augmentation has no effect on gradient flow or the optimization landscape.

**Q: Your CNN and ResNet have different param counts — doesn't that invalidate the comparison?**  
Partially, and this is documented as a known limitation. But Claim 1 (CNN-56 < CNN-20) is self-contained — it involves only the CNN family and stands independently of any ResNet comparison.

**Q: What would happen at 100 layers?**  
Plain CNN: severe degradation. Near-zero gradient signal in early layers. Trains worse than a 20-layer version. ResNet: the additive identity path remains intact at any depth — demonstrated up to 1000+ layers in the paper.

---

*Reference: He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep Residual Learning for Image Recognition. CVPR 2016.*
