# Adaptive Learning System Documentation

## Abstract
This document presents a formal description of an adaptive learning system for Python education that integrates knowledge tracing, behavior-aware recommendation, retrieval-augmented tutoring, and engagement mechanisms. The system maintains topic-level mastery estimates, uses behavioral intelligence signals to modulate difficulty, and evaluates outcomes through longitudinal metrics and controlled experimentation. The exposition emphasizes mathematical definitions, explainable decision logic, and a reproducible evaluation framework suitable for peer review.

## 1. Introduction
Adaptive learning systems require accurate modeling of learner knowledge, dynamic content sequencing, and robust evaluation of educational impact. The system described here targets foundational and intermediate Python learning, combining a probabilistic mastery model with a behavior-informed recommendation engine. The architecture is designed for explainability, with explicit feature weights and decision thresholds, and it provides formal evaluation metrics spanning learning gain, mastery slope, time-to-mastery, and difficulty-shift outcomes.

## 2. Related Work (Brief)
Prior work on adaptive learning commonly leverages Bayesian Knowledge Tracing (BKT), Item Response Theory (IRT), and deep knowledge tracing. Recommendation strategies often incorporate mastery gaps, prerequisite graphs, and engagement signals. Retrieval-augmented generation (RAG) approaches have also been applied to instructional tutoring, combining vector search with constrained response synthesis to reduce hallucinations. The present system aligns with these paradigms while prioritizing feature-level interpretability and operational simplicity.

## 3. System Architecture Overview
The system is implemented as a web-based learning platform with a Django REST backend, a React client, and a PostgreSQL database. The adaptive components include:
- Knowledge tracing and mastery storage in user profiles.
- Behavior tracking at the topic level, including response time, hints, and failure streak.
- Recommendation services that compute priority scores and apply difficulty adaptation.
- A RAG tutor that retrieves lesson chunks via pgvector similarity search and produces responses with citations.
- Gamification services that maintain engagement scores and progression signals.
The architecture maintains explicit logs for recommendations and difficulty shifts to support evaluation and auditing.

## 4. Knowledge Tracing Model
### 4.1 Bayesian Update Formulation
Let \( p_t \in [0, 1] \) denote the mastery probability for a topic at time \( t \). The system applies a Bayesian-style update with two parameters: a learning rate \( \lambda \) and a slip factor \( s \). Given an observation \( o_t \in \{0,1\} \) representing incorrect or correct performance:
- If \( o_t = 1 \) (correct):  
  \( p_{t+1} = p_t + (1 - p_t)\lambda \)
- If \( o_t = 0 \) (incorrect):  
  \( p_{t+1} = p_t \cdot s \)

This formulation retains the Bayesian intuition of posterior updating while using a compact parametric form for robustness and interpretability.

### 4.2 Mastery Probability Interpretation
The mastery probability \( p_t \) represents the system’s belief that the learner can correctly answer questions in the topic without assistance. It is persisted in the user’s mastery vector and is used both to select topics for recommendation and to evaluate mastery progression over time.

## 5. Recommendation Engine
### 5.1 Priority Score Formula
The recommendation engine computes a priority score for each topic. Two strategy variants are supported for A/B testing.

Strategy A:
\[
S = 0.35(1 - m) + 0.15 f + 0.15 r + 0.15 e + 0.10 v + 0.10 s + d
\]

Strategy B:
\[
S = 0.40(1 - m) + 0.10 f + 0.10 r + 0.20 e + 0.15 v + 0.05 s + d
\]

Where:
- \( m \): mastery estimate for the topic
- \( f \): recent failure rate
- \( r \): prerequisite dependency weight
- \( e \): engagement factor
- \( v \): learning velocity weight (normalized)
- \( s \): struggle weight
- \( d \): difficulty adjustment factor

### 5.2 Difficulty Adaptation Model
Difficulty adaptation is computed as a behavior-aware override on the base difficulty without modifying mastery. A downgrade is triggered if any struggle indicator is active:
- failure streak \( \geq \tau_f \)
- learning velocity \( < \tau_v \)
- average response time \( \geq \tau_t \)
- average hints used \( \geq \tau_h \)

An upgrade to challenge-level content is triggered when:
1) mastery \( > 0.8 \),  
2) learning velocity \( > \tau_v^{high} \), and  
3) average response time \( \leq \tau_t^{low} \).

Difficulty transitions are logged with reason codes to preserve explainability and to support post-hoc evaluation.

### 5.3 Learning Velocity Definition
Learning velocity is defined as:
\[
v_t = \frac{m_t - m_{t-1}}{\Delta t}
\]
where \( \Delta t \) is the elapsed time between mastery updates. A rolling average is maintained per topic using exponential smoothing:
\[
\bar{v}_t = \alpha v_t + (1 - \alpha)\bar{v}_{t-1}
\]
The system also maintains a user-level velocity aggregate using a second smoothing factor to preserve a global learning-rate signal.

## 6. RAG Tutor Architecture
### 6.1 Embedding Generation
Lesson text is chunked and embedded with a pluggable provider: OpenAI embeddings, local sentence-transformer embeddings, or a deterministic hashing fallback. Embeddings are normalized to a fixed dimension for consistent vector search.

### 6.2 pgvector Similarity Search
For a query \( q \), the system computes an embedding \( \mathbf{e}_q \) and retrieves top-\( k \) chunks using pgvector distance metrics (cosine or L2). Retrieved chunks are filtered by a similarity threshold \( \theta \) to enforce relevance.

### 6.3 Confidence Scoring
Confidence is computed as a monotonic function of the number of high-similarity retrieved chunks. The default policy uses a base confidence plus an increment per retrieved chunk, capped at a fixed maximum to prevent overconfidence.

### 6.4 Hallucination Prevention Strategy
The tutor returns a fallback response when retrieval yields no high-similarity context. Responses include source snippets and similarity metadata, enabling transparent attribution. The model is constrained to retrieved content, reducing hallucination risk.

## 7. Gamification & Engagement Model
The system maintains an engagement score \( e \in [0,1] \) updated via bounded additive deltas:
\[
e_{t+1} = \min(1, \max(0, e_t + \Delta e))
\]
Engagement analytics also include an index that aggregates user interactions, providing a normalized engagement signal for recommendations and reporting.

## 8. Evaluation Framework
### 8.1 A/B Testing Design
Users are deterministically assigned to strategy A or B based on an invariant user identifier parity. The assignment is stored to ensure consistent exposure across sessions.

### 8.2 Learning Gain Metric
Learning gain is computed from diagnostic assessments as:
\[
G = \text{PostTest} - \text{PreTest}
\]
where each score is normalized to \([0,1]\).

### 8.3 Mastery Improvement Slope
The mastery improvement slope is computed as the average change in mastery per day across completed recommendations:
\[
S_m = \frac{m_{last} - m_{first}}{\Delta t_{days}}
\]

### 8.4 Time-to-Mastery
Time-to-mastery is defined as the elapsed time between user registration and the earliest timestamp at which any topic mastery exceeds a target threshold (default 0.8).

### 8.5 Downgrade Effectiveness
Downgrade effectiveness is defined as the proportion of downgrades after which mastery increases:
\[
E_d = \frac{\#(\Delta m > 0 \mid \text{downgrade})}{\#(\text{downgrade evaluated})}
\]

### 8.6 Velocity Distribution
Velocity distribution is reported as counts of topic velocities in low, medium, and high bins derived from configured thresholds, along with the mean velocity.

## 9. Experimental Design
### 9.1 Pilot Study Setup
The pilot study enrolls learners at beginner and intermediate levels and collects baseline diagnostics, activity logs, and RAG interaction data. The system records mastery updates, difficulty shifts, and recommendation outcomes.

### 9.2 Control vs Adaptive Groups
Control group users receive recommendations without behavioral difficulty adaptation. Adaptive group users receive recommendations with dynamic difficulty adjustments based on behavioral intelligence signals.

### 9.3 Evaluation Methodology
Outcomes are compared using pre/post learning gains, mastery slope, and completion rates. Difficulty shift success is analyzed to validate the efficacy of downgrades and challenge escalations.

## 10. Results Metrics Definition
The system reports the following metrics:
- Recommendation precision: completed recommendations over accepted recommendations.
- Mean learning gain: mean diagnostic improvement across users.
- Engagement improvement: normalized engagement growth per day.
- Average time-to-mastery: mean time to reach mastery threshold.
- Mastery improvement slope: mean slope of mastery progression.
- Total downgrades and upgrades: counts of difficulty shifts.
- Difficulty shift success rate: proportion of downgrades with post-shift mastery improvement.
- Downgrade effectiveness: evaluated success rate with totals and denominators.
- Velocity distribution: low/medium/high counts and mean velocity.
- Challenge problem success rate: proportion of challenge shifts with non-decreasing mastery.

## 11. Limitations
The knowledge tracing update uses a compact parametric form rather than a full Bayesian model with slip and guess probabilities. Behavioral thresholds are currently fixed and may require calibration across cohorts. The RAG system relies on text chunking quality and embedding coverage, which can affect retrieval recall.

## 12. Future Work
Future extensions include: calibrated BKT with explicit guess/slip parameters, adaptive threshold tuning via Bayesian optimization, personalized difficulty schedules, and rigorous randomized controlled trials at scale. Additional work may incorporate richer engagement models that include streaks, badges, and session-level persistence.

## 13. Conclusion
This document formalizes an adaptive learning system that integrates knowledge tracing, behavior-informed recommendations, and RAG tutoring within a cohesive, explainable architecture. The system provides explicit metrics for evaluation and supports controlled experimentation, establishing a foundation for research-grade analysis of adaptive learning outcomes.
