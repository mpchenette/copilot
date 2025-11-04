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
            Assert.Equal(15, score);
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
    }
}