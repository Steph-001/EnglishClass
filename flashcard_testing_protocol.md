# Flashcard System Testing Protocol

## Phase 1: Basic Functionality Tests

### ✅ Initial Load & Display
- [ ] Page loads without errors (check browser console)
- [ ] Cards display correctly with stressed vowels (red highlighting)
- [ ] All UI elements are visible and properly styled
- [ ] Progress stats show: Reviewed: 0, Again: 0, Hard: 0, Medium: 0, Easy: 0, Due: [total cards]
- [ ] Card counter shows "1 / [total]"

### ✅ Card Navigation (Browse Mode)
- [ ] Click card to flip - shows answer side
- [ ] Click again to flip back to question
- [ ] "Next →" button advances to next card
- [ ] "← Previous" button goes to previous card
- [ ] Navigation buttons disable at start/end appropriately
- [ ] Card counter updates correctly (2/5, 3/5, etc.)

### ✅ Study Mode Toggle
- [ ] Click "📖 Browse" button
- [ ] Button changes to "📚 Studying" 
- [ ] Difficulty buttons appear (Again, Hard, Medium, Easy)
- [ ] Cards are shuffled (different order than browse)
- [ ] Due count shows available cards

## Phase 2: 4-Level SM-2 Algorithm Tests

### ✅ Create Test Deck (5-10 cards minimum)

### ✅ Test Each Difficulty Level
**Test "Again" (🚫):**
- [ ] Flip card, click "Again"
- [ ] Card stays in session (doesn't disappear)
- [ ] "Again" counter increments
- [ ] Next card appears
- [ ] Check database: `interval: 0.007`, `easeFactor` reduced by 0.20

**Test "Hard" (😰):**
- [ ] Flip card, click "Hard" 
- [ ] Card removed from session
- [ ] "Hard" counter increments
- [ ] Check database: `interval: 1`, `easeFactor` reduced by 0.15

**Test "Medium" (🤔):**
- [ ] Flip card, click "Medium"
- [ ] Card removed from session  
- [ ] "Medium" counter increments
- [ ] Check database: `interval: 1` (first review), `easeFactor` reduced by 0.05

**Test "Easy" (😊):**
- [ ] Flip card, click "Easy"
- [ ] Card removed from session
- [ ] "Easy" counter increments  
- [ ] Check database: `interval: 2` (first review), `easeFactor` increased by 0.15

### ✅ Verify Data Structure
Open browser DevTools → Console, run:
```javascript
console.log('Card Data:', window.flashcardSystem.cardData);
console.log('Session Stats:', window.flashcardSystem.sessionStats);
```

Expected format:
```json
{
  "0": {
    "interval": 1,
    "easeFactor": 2.35,
    "reviewCount": 1,
    "lastReviewed": 1753896390914,
    "nextReview": 1753982790914
  }
}
```

## Phase 3: Session Completion & Early Review

### ✅ Complete Study Session
- [ ] Review all due cards
- [ ] Completion modal appears with "🎉 Great Job!"
- [ ] Shows next review time estimate
- [ ] "⏰ Review Early Cards" button appears if applicable
- [ ] "📖 Browse All Cards" works
- [ ] "✨ Done" closes modal

### ✅ Early Review System
- [ ] Test early review button functionality
- [ ] Only cards due within 24 hours appear
- [ ] Cards shuffle properly for early review

## Phase 4: Data Persistence Tests

### ✅ Local Storage Backup
- [ ] Review some cards
- [ ] Refresh page
- [ ] Progress maintained (card positions, stats, reviewed cards)
- [ ] Check localStorage: `flashcards_[setId]` exists with valid JSON

### ✅ Supabase Integration (If Logged In)
- [ ] Log in to system
- [ ] Review some cards  
- [ ] Check Supabase dashboard: `flashcard_progress` table updated
- [ ] Log out and back in: progress restored
- [ ] Test on different device/browser: data syncs

### ✅ Data Migration (Backward Compatibility)
**If you have existing 3-level data:**
- [ ] Old data loads without errors
- [ ] Missing "again", "hard", "medium" stats default to 0
- [ ] New 4-level system works with migrated data

## Phase 5: UI/UX Tests

### ✅ Mobile Responsiveness
- [ ] Test on phone (< 480px width)
- [ ] Difficulty buttons wrap properly
- [ ] Progress stats display in grid format
- [ ] Cards remain readable and interactive
- [ ] All buttons remain clickable

### ✅ Study Mode Behavior
- [ ] Difficulty buttons only show in study mode
- [ ] Difficulty buttons hidden in browse mode
- [ ] Can't accidentally mark difficulty while browsing

### ✅ Edge Cases
- [ ] Test with 1 card deck
- [ ] Test with empty deck (no lexicon data)
- [ ] Test rapid clicking (no double-processing)
- [ ] Test flipping before marking difficulty

## Phase 6: Authentication Edge Cases

### ✅ Auth State Changes
- [ ] Login while using system: data syncs
- [ ] Logout while using system: continues with localStorage
- [ ] Network disconnection: graceful fallback to localStorage
- [ ] Multiple tabs: no conflicts or data corruption

## Phase 7: Performance & Error Handling

### ✅ Browser Console Check
- [ ] No JavaScript errors during normal use
- [ ] No 404s or failed network requests
- [ ] Supabase connection errors handled gracefully

### ✅ Stress Testing
- [ ] Rapid card flipping (no UI lag)
- [ ] Quick difficulty marking (no double-saves)
- [ ] Large deck performance (50+ cards)

## Testing Checklist Summary

### Pre-Deployment:
- [ ] All Phase 1-7 tests passed
- [ ] No console errors
- [ ] Mobile testing completed
- [ ] Supabase data verified
- [ ] Backward compatibility confirmed

### Post-Deployment Monitoring:
- [ ] Check first few real user sessions
- [ ] Monitor Supabase logs for errors
- [ ] Verify stats tracking accuracy
- [ ] Confirm SM-2 intervals are reasonable

### Emergency Rollback Plan:
- [ ] Keep backup of working 3-level system
- [ ] Document rollback procedure
- [ ] Test rollback on staging environment

---

## Quick Test Script

For rapid testing, review 5 cards in this order:
1. Card 1: **Again** → should stay in session
2. Card 2: **Hard** → should disappear, next review in 1 day  
3. Card 3: **Medium** → should disappear, next review in 1 day
4. Card 4: **Easy** → should disappear, next review in 2 days
5. Card 5: **Again** → should stay in session

**Expected final stats:** Reviewed: 4, Again: 2, Hard: 1, Medium: 1, Easy: 1, Due: 0