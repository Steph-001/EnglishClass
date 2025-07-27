---
title: "tests"
date: 2025-07-26
tags: [flashcards]
---

# tests

Core Functionality Tests
1. Regular Study Mode

 Reset progress, study all cards normally
 Verify counters update correctly during study
 Check that cards get proper intervals (1→3→calculated days)
 Confirm completion message shows when done
 Verify data saves to localStorage and Supabase

2. Early Review (Fixed)

 After regular study, verify early review button appears
 Early review cards show correct content
 Counters update properly during early review ✅ (Fixed)
 Card intervals update correctly during early review
 Data saves properly after early reviews

3. SM-2 Algorithm Accuracy

 Mark card as Easy: interval should be 2→4→(4×easeFactor) days
 Mark card as Medium: interval should be 1→3→(3×easeFactor) days
 Mark card as Hard: interval resets to 1 day, easeFactor decreases
 Verify easeFactor adjustments (+0.15 easy, -0.05 medium, -0.15 hard)

4. Timing Tests

 Cards due "now" appear in regular study
 Cards due within 24h (but not now) appear in early review only
 Cards not due within 24h don't appear in either mode
 Wait for actual interval to pass, verify card becomes due again

Data Persistence Tests
5. localStorage (Offline)

 Disconnect internet, verify everything still works
 Data persists across browser refresh
 Multiple deck data doesn't interfere

6. Supabase Sync (Online)

 Login, verify data syncs to Supabase
 Check Supabase dashboard shows correct data
 Logout/login, verify data loads from Supabase
 Test conflict resolution (newer localStorage vs database)

7. Auth State Changes

 Study while logged out, then login → data should migrate
 Study while logged in, logout → should fallback to localStorage
 Multiple browser tabs with different auth states

UI/UX Tests
8. Mode Switching

 Browse → Study → Browse transitions work correctly
 Button states update properly
 Card order changes correctly between modes

9. Study Mode Variations

 Term→Definition mode works
 Definition→Term mode works
 Mode switching preserves progress

10. Edge Cases

 What happens with 0 cards due?
 What happens when all cards are mastered (long intervals)?
 Rapid clicking on difficulty buttons
 Browser refresh during study session

Cross-Session Tests
11. Long-term Behavior

 Study cards, wait 24+ hours, verify they become due again
 Cards marked "easy" should have longer intervals than "hard" cards
 Session stats reset properly between sessions
 Global progress persists across sessions

12. Multi-Deck Testing

 Multiple Hugo pages with different lexicon data
 Each deck maintains separate progress
 No data bleed between decks
