# Adaptive Python Learning Assistant - Complete Refactor TODO

## 🎯 EXECUTION STATUS
- [ ] Phase 1: Data Models ✅
- [ ] Phase 2: Submission Pipeline  
- [ ] Phase 3: Learning Intelligence
- [ ] Phase 4: Analytics Fix
- [ ] Phase 5: Evaluation Engine
- [ ] Phase 6: Recommendation Engine
- [ ] Phase 7: Frontend Integration
- [ ] Final Testing & Cleanup

---

## 🗄️ PHASE 1: DATA MODEL FIX (CRITICAL - RELATIONAL INTEGRITY)

### 1.1 Create/Update Models (backend/core/models.py)
```
✅ [ ] Add Topic model (id, name, canonical_name, description, order)
✅ [ ] Add UserSubmission model 
   - user FK(User)
   - topic FK(Topic) 
   - challenge FK(Challenge,null=True)
   - code TEXT
   - score FloatField
   - passed_tests IntegerField
   - total_tests IntegerField
   - attempts IntegerField (computed)
   - created_at DateTimeField
   - indexes: (user,challenge), (user,topic)
✅ [ ] Refactor UserProgress:
   - user_id(TextField) → user FK(User)
   - lesson_id(Int) → lesson FK(Lesson,null=True)
   - ADD topic FK(Topic)
```

### 1.2 Serializers (backend/core/serializers.py)
```
✅ [ ] TopicSerializer
✅ [ ] UserSubmissionSerializer  
✅ [ ] Update UserProgressSerializer (userId→user)
```

### 1.3 Database Migration
```
⚠️  CRITICAL: Backup/Restore DB due to FK changes
✅ [ ] cd backend && python manage.py makemigrations core
✅ [ ] Review migration: data migration user_id→user_id FK
✅ [ ] python manage.py migrate
✅ [ ] python manage.py showmigrations (verify applied)
```

### 1.4 Seed Topics (backend/core/management/commands/seed_topics.py)
```
✅ [ ] Create predefined topics:
   variables, conditions, loops, functions, data_structures, oop
✅ [ ] python manage.py seed_topics
```

### 1.5 Phase 1 Testing
```
✅ [ ] Server starts: python manage.py runserver
✅ [ ] API: GET /api/topics/ (new endpoint)
✅ [ ] Django shell: verify UserProgress.user FK works
```

---

## 🔄 PHASE 2: SUBMISSION PIPELINE (TRANSACTIONAL)

### 2.1 Views & URLs (backend/core/views.py, urls.py)
```
✅ [ ] UserSubmissionViewSet (create/list)
✅ [ ] Enhance RunChallengeView:
   |→ @transaction.atomic()
   |→ Create UserSubmission
   |→ Increment attempts (UserSubmission.filter().count())
   |→ Update/Create UserProgress  
   |→ add_xp() + update_streak()
   |→ Trigger skill gap analysis
✅ [ ] router.register('user-submissions')
```

### 2.2 Phase 2 Testing
```
✅ [ ] POST /api/user-submissions/ → DB records created
✅ [ ] Code submit → XP increases, streak updates
```

---

## 🧠 PHASE 3: LEARNING INTELLIGENCE

### 3.1 Mastery & Skill Gaps (analytics/services/skill_analysis.py)
```
✅ [ ] analyze_user_skill_gaps(): use UserSubmission data
✅ [ ] Update mastery_vector post-submission
✅ [ ] Auto-save SkillGapAnalysis
```

---

## 📊 PHASE 4: ANALYTICS FIX

### 4.1 Real Data Services (analytics/analytics_services.py)
```
✅ [ ] mastery_progression(): prioritize UserSubmission
✅ [ ] learning_gain(): submission-based computation
✅ [ ] Remove excessive synthetic fallbacks
```

---

## ⚗️ PHASE 5: EVALUATION ENGINE

### 5.1 Fallback Metrics (evaluation/services.py)
```
✅ [ ] Recent UserSubmission → simple scoring fallback
✅ [ ] Reduce 'insufficient_data' responses
```

---

## 🎯 PHASE 6: RECOMMENDATION ENGINE

### 6.1 Submission Integration (recommendation/services.py)
```
✅ [ ] recent_failure(): scan UserSubmission
✅ [ ] update_topic_velocity() post-submit
```

---

## 🎨 PHASE 7: FRONTEND INTEGRATION

### 7.1 Dashboard (client/src/pages/Dashboard.tsx)
```
✅ [ ] Recent Submissions table
✅ [ ] Real-time refetch post-submit
✅ [ ] Submission history API integration
```

---

## ✅ FINAL TESTING CHECKLIST

```
[ ] Reset DB: python manage.py flush → migrate → seed
[ ] E2E Flow:
  |→ Code submission → UserSubmission saved
  |→ UserProgress updated  
  |→ XP/Streak/Badges awarded
  |→ SkillGapAnalysis generated
  |→ Dashboard shows real data
  |→ Recommendations adaptive
[ ] Performance: Indexes working (EXPLAIN queries)
[ ] APIs standardized (200 OK, JSON responses)
[ ] Frontend: No hardcoded data
[ ] Error handling: Transactions rollback on failure
```

## ✅ PHASE 1 PROGRESS

**1.1 Models**: ✅ Topic, UserSubmission added + UserProgress FKs + indexes  
**1.2 Serializers**: ✅ TopicSerializer, UserSubmissionSerializer, UserProgressSerializer  
**1.3 Migrations**: ✅ 0020 applied (fresh DB + FKs/indexes)  
**1.4 Seed Topics**: ✅ 6 topics seeded  
**1.5 Testing**: ✅ APIs ready (/topics/, /user-submissions/)

**PHASE 1 ✅ COMPLETE**
**PHASE 2.1**: ✅ ViewSets + URLs (/api/topics/, /api/user-submissions/)
**PHASE 2.2**: ✅ Transactional pipeline (@atomic, submission→progress→XP→analytics)

**PHASE 2 ✅ COMPLETE**
**PHASE 3.1**: ✅ mastery_progression() uses UserSubmission + UserProgress
**PHASE 3.2**: ✅ skill_analysis.py accuracy from submissions (score≥80%)
**PHASE 3 ✅ COMPLETE**

**PHASE 4**: 🔄 Frontend Dashboard (recent submissions table)
**1.5 Testing**: ⏳
**1.5 Testing**: ⏳

---

**Next**: `cd backend && python manage.py makemigrations core`

