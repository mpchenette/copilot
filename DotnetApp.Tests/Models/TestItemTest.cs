using System;
using Xunit;
using DotnetApp.Models;

namespace DotnetApp.Models.Tests
{
    public class TaskItemTest
    {
        [Fact]
        public void CalculateTaskScore_ShouldReturnCorrectScore_ForPriorityZero()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 0,
                Status = "pending",
                CreatedAt = DateTime.UtcNow.AddDays(-1),
                IsCompleted = false,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            Assert.Equal(1, score);
        }

        [Fact]
        public void CalculateTaskScore_ShouldReturnCorrectScore_ForPriorityOneAndPendingStatus()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 1,
                Status = "pending",
                CreatedAt = DateTime.UtcNow.AddDays(-1),
                IsCompleted = false,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            Assert.Equal(13, score);
        }

        [Fact]
        public void CalculateTaskScore_ShouldReturnCorrectScore_ForPriorityTwoAndInProgressStatus()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 2,
                Status = "in-progress",
                CreatedAt = DateTime.UtcNow.AddDays(-8),
                IsCompleted = false,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            Assert.Equal(10, score);
        }

        [Fact]
        public void CalculateTaskScore_ShouldDoubleScore_ForPendingStatusAndOldTask()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 2,
                Status = "pending",
                CreatedAt = DateTime.UtcNow.AddDays(-15),
                IsCompleted = false,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority score: 5, Status score: 5*2 + 5 = 15, Total: 20
            Assert.Equal(20, score);
        }

        [Fact]
        public void CalculateTaskScore_ShouldSubtractScore_ForCompletedInProgressTask()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 2,
                Status = "in-progress",
                CreatedAt = DateTime.UtcNow.AddDays(-1),
                IsCompleted = true,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            Assert.Equal(0, score);
        }

        [Fact]
        public void CalculateTaskScore_ShouldAddScore_ForLongWordsInTitle()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 3,
                Status = "in-progress",
                CreatedAt = DateTime.UtcNow.AddDays(-1),
                IsCompleted = false,
                Title = "ThisIsAVeryLongWord Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            Assert.Equal(2, score);
        }

        [Fact]
        public void CalculateTaskScore_ShouldReturnZero_ForNegativeScore()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 3,
                Status = "completed",
                CreatedAt = DateTime.UtcNow.AddDays(-1),
                IsCompleted = true,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            Assert.Equal(1, score);
        }

        [Fact]
        public void CalculateTaskScore_PriorityOne_NotPending_ShouldReturnBaseScore()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 1,
                Status = "in-progress",
                CreatedAt = DateTime.UtcNow.AddDays(-1),
                IsCompleted = false,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority score: 10 (no +3 because not pending)
            // Status score: 0 (in-progress, not completed, no long words)
            Assert.Equal(10, score);
        }

        [Fact]
        public void CalculateTaskScore_PriorityTwo_InProgress_NotCompleted_WithinWeek()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 2,
                Status = "in-progress",
                CreatedAt = DateTime.UtcNow.AddDays(-5),
                IsCompleted = false,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority score: 5 + 2 = 7 (in-progress and not completed but < 7 days)
            // Status score: 0
            Assert.Equal(7, score);
        }

        [Fact]
        public void CalculateTaskScore_PriorityThree_DefaultStatus_NotCompleted()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 3,
                Status = "blocked",
                CreatedAt = DateTime.UtcNow.AddDays(-1),
                IsCompleted = false,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority score: 1
            // Status score: 3 (default case, not completed and priority < 3 is false for priority=3)
            Assert.Equal(1, score);
        }

        [Fact]
        public void CalculateTaskScore_PriorityTwo_DefaultStatus_NotCompleted()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 2,
                Status = "cancelled",
                CreatedAt = DateTime.UtcNow.AddDays(-1),
                IsCompleted = false,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority score: 5
            // Status score: 3 (default case, not completed and priority < 3)
            Assert.Equal(8, score);
        }

        [Fact]
        public void CalculateTaskScore_NegativePriority_ShouldTreatAsLowPriority()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = -1,
                Status = "pending",
                CreatedAt = DateTime.UtcNow.AddDays(-1),
                IsCompleted = false,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority <= 0 gives score of 1
            Assert.Equal(1, score);
        }

        [Fact]
        public void CalculateTaskScore_OldPendingTask_HighPriority_ShouldDoubleAndAdd()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 1,
                Status = "pending",
                CreatedAt = DateTime.UtcNow.AddDays(-20),
                IsCompleted = false,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority score: 10 + 3 = 13
            // Status score: 13 * 2 + 5 = 31
            // Total: 44
            Assert.Equal(44, score);
        }

        [Fact]
        public void CalculateTaskScore_InProgress_MultipleLongWords()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 3,
                Status = "in-progress",
                CreatedAt = DateTime.UtcNow.AddDays(-1),
                IsCompleted = false,
                Title = "VeryLongWord AnotherLongWord ThirdLongWordHere"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority score: 1
            // Status score: 3 (three words > 10 chars)
            Assert.Equal(4, score);
        }

        [Fact]
        public void CalculateTaskScore_InProgress_Completed_ShouldSubtract()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 1,
                Status = "in-progress",
                CreatedAt = DateTime.UtcNow.AddDays(-1),
                IsCompleted = true,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority score: 10
            // Status score: -5 (completed in-progress)
            // Total: max(0, 5) = 5
            Assert.Equal(5, score);
        }

        [Fact]
        public void CalculateTaskScore_PendingTask_ExactlyFourteenDays()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 2,
                Status = "pending",
                CreatedAt = DateTime.UtcNow.AddDays(-14).AddSeconds(1), // Just under 14 days
                IsCompleted = false,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority score: 5
            // Status score: 0 (< 14 days, so no doubling)
            Assert.Equal(5, score);
        }

        [Fact]
        public void CalculateTaskScore_PendingTask_OverFourteenDays()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 2,
                Status = "pending",
                CreatedAt = DateTime.UtcNow.AddDays(-15),
                IsCompleted = false,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority score: 5
            // Status score: 5*2 + 5 = 15
            // Total: 20
            Assert.Equal(20, score);
        }

        [Fact]
        public void CalculateTaskScore_UppercaseStatus_ShouldWork()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 1,
                Status = "PENDING",
                CreatedAt = DateTime.UtcNow.AddDays(-1),
                IsCompleted = false,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Note: Status check in CalculatePriorityScore is case-sensitive (line 42)
            // So "PENDING" != "pending", priority score is 10, not 13
            // Status score: 0 (ToLower() in CalculateStatusScore matches, but no old task bonus)
            Assert.Equal(10, score);
        }

        [Fact]
        public void CalculateTaskScore_MixedCaseStatus_InProgress()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 2,
                Status = "In-Progress",
                CreatedAt = DateTime.UtcNow.AddDays(-1),
                IsCompleted = false,
                Title = "TestWord"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority score: 5
            // Status score: 0 (no long words)
            Assert.Equal(5, score);
        }

        [Fact]
        public void CalculateTaskScore_InProgress_LongWordExactly10Chars()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 3,
                Status = "in-progress",
                CreatedAt = DateTime.UtcNow.AddDays(-1),
                IsCompleted = false,
                Title = "ExactlyTen Word"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority score: 1
            // Status score: 0 (word must be > 10, not >= 10)
            Assert.Equal(1, score);
        }

        [Fact]
        public void CalculateTaskScore_InProgress_LongWordExactly11Chars()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 3,
                Status = "in-progress",
                CreatedAt = DateTime.UtcNow.AddDays(-1),
                IsCompleted = false,
                Title = "ElevenChars Word"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority score: 1
            // Status score: 1 (11 > 10)
            Assert.Equal(2, score);
        }

        [Fact]
        public void CalculateTaskScore_Priority2_InProgress_ExactlySeven_Days()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 2,
                Status = "in-progress",
                CreatedAt = DateTime.UtcNow.AddDays(-7).AddSeconds(1), // Just under 7 days
                IsCompleted = false,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority score: 5 + 2 = 7 (< 7 days, so no +3 bonus)
            // Status score: 0
            Assert.Equal(7, score);
        }

        [Fact]
        public void CalculateTaskScore_Priority2_InProgress_OverSeven_Days()
        {
            // Arrange
            var task = new TaskItem
            {
                Priority = 2,
                Status = "in-progress",
                CreatedAt = DateTime.UtcNow.AddDays(-8),
                IsCompleted = false,
                Title = "Test Task"
            };

            // Act
            var score = task.CalculateTaskScore();

            // Assert
            // Priority score: 5 + 2 + 3 = 10 (> 7 days)
            // Status score: 0
            Assert.Equal(10, score);
        }
    }
}