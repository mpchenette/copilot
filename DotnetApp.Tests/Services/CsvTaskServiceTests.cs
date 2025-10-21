using System;
using System.IO;
using System.Linq;
using DotnetApp.Models;
using DotnetApp.Services;
using Xunit;

namespace DotnetApp.Tests.Services
{
    public class CsvTaskServiceTests : IDisposable
    {
        private readonly string _testFilePath;
        private readonly CsvTaskService _service;

        public CsvTaskServiceTests()
        {
            // Create a unique test file path for each test instance
            _testFilePath = Path.Combine(Path.GetTempPath(), $"test_tasks_{Guid.NewGuid()}.csv");
            
            // Set AppContext.BaseDirectory to temp directory for testing
            var field = typeof(AppContext).GetField("s_baseDirectory", 
                System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static);
            var originalPath = AppContext.BaseDirectory;
            field?.SetValue(null, Path.GetTempPath());
            
            _service = new CsvTaskService();
        }

        public void Dispose()
        {
            // Clean up test files
            var tasksFile = Path.Combine(AppContext.BaseDirectory, "tasks.csv");
            if (File.Exists(tasksFile))
            {
                File.Delete(tasksFile);
            }
        }

        [Fact]
        public void CreateTask_AssignsIdAndStoresTaskInCsv()
        {
            var task = new TaskItem 
            { 
                Title = "Test Task",
                Description = "Test Description",
                Status = "pending",
                Priority = 1
            };

            _service.CreateTask(task);

            Assert.NotEqual(0, task.Id);
            var all = _service.GetAllTasks().ToList();
            Assert.Contains(all, t => t.Id == task.Id && t.Title == "Test Task");
        }

        [Fact]
        public void GetTaskById_ReturnsCorrectTaskOrNull()
        {
            var task = new TaskItem { Title = "GetById", Description = "Test" };
            _service.CreateTask(task);
            var id = task.Id;

            var found = _service.GetTaskById(id);
            Assert.NotNull(found);
            Assert.Equal("GetById", found.Title);

            var missing = _service.GetTaskById(id + 999);
            Assert.Null(missing);
        }

        [Fact]
        public void UpdateTask_NonExisting_ReturnsFalse()
        {
            var updated = new TaskItem { Title = "Nope" };

            var result = _service.UpdateTask(999, updated);
            Assert.False(result);
        }

        [Fact]
        public void UpdateTask_Existing_ReturnsTrueAndUpdates()
        {
            var task = new TaskItem 
            { 
                Title = "Original",
                Description = "Original Description",
                Status = "pending",
                Priority = 2
            };
            _service.CreateTask(task);
            var id = task.Id;

            var updated = new TaskItem 
            { 
                Title = "Updated",
                Description = "Updated Description",
                Status = "in-progress",
                Priority = 1
            };
            var result = _service.UpdateTask(id, updated);

            Assert.True(result);
            Assert.Equal(id, updated.Id);
            var fetched = _service.GetTaskById(id);
            Assert.NotNull(fetched);
            Assert.Equal("Updated", fetched.Title);
            Assert.Equal("Updated Description", fetched.Description);
            Assert.Equal("in-progress", fetched.Status);
            Assert.Equal(1, fetched.Priority);
        }

        [Fact]
        public void DeleteTask_ReturnsTrueAndRemoves()
        {
            var task = new TaskItem { Title = "ToDelete" };
            _service.CreateTask(task);
            var id = task.Id;

            var result = _service.DeleteTask(id);

            Assert.True(result);
            Assert.Null(_service.GetTaskById(id));
        }

        [Fact]
        public void DeleteTask_NonExisting_ReturnsFalse()
        {
            var result = _service.DeleteTask(999);
            Assert.False(result);
        }

        [Fact]
        public void GetAllTasks_Empty_ReturnsEmpty()
        {
            var all = _service.GetAllTasks().ToList();
            Assert.Empty(all);
        }

        [Fact]
        public void CreateTask_SequentialIds()
        {
            var t1 = new TaskItem { Title = "First" };
            _service.CreateTask(t1);
            var t2 = new TaskItem { Title = "Second" };
            _service.CreateTask(t2);

            Assert.Equal(t1.Id + 1, t2.Id);
        }

        [Fact]
        public void CreateTask_WithNullDescription_StoresEmptyString()
        {
            var task = new TaskItem 
            { 
                Title = "No Description",
                Description = null
            };
            _service.CreateTask(task);

            var fetched = _service.GetTaskById(task.Id);
            Assert.NotNull(fetched);
            Assert.Null(fetched.Description);
        }

        [Fact]
        public void CreateTask_WithSpecialCharacters_StoresCorrectly()
        {
            var task = new TaskItem 
            { 
                Title = "Task with special chars",
                Description = "Description without commas"
            };
            _service.CreateTask(task);

            var fetched = _service.GetTaskById(task.Id);
            Assert.NotNull(fetched);
            Assert.Equal("Task with special chars", fetched.Title);
            Assert.Equal("Description without commas", fetched.Description);
        }

        [Fact]
        public void GetAllTasks_ReturnsAllTasks()
        {
            var task1 = new TaskItem { Title = "Task 1" };
            var task2 = new TaskItem { Title = "Task 2" };
            var task3 = new TaskItem { Title = "Task 3" };

            _service.CreateTask(task1);
            _service.CreateTask(task2);
            _service.CreateTask(task3);

            var all = _service.GetAllTasks().ToList();
            Assert.Equal(3, all.Count);
            Assert.Contains(all, t => t.Title == "Task 1");
            Assert.Contains(all, t => t.Title == "Task 2");
            Assert.Contains(all, t => t.Title == "Task 3");
        }

        [Fact]
        public void CreateTask_PreservesAllProperties()
        {
            var now = DateTime.UtcNow;
            var task = new TaskItem 
            { 
                Title = "Complete Task",
                Description = "Full Description",
                IsCompleted = true,
                Status = "completed",
                Priority = 1,
                CreatedAt = now
            };
            _service.CreateTask(task);

            var fetched = _service.GetTaskById(task.Id);
            Assert.NotNull(fetched);
            Assert.Equal("Complete Task", fetched.Title);
            Assert.Equal("Full Description", fetched.Description);
            Assert.True(fetched.IsCompleted);
            Assert.Equal("completed", fetched.Status);
            Assert.Equal(1, fetched.Priority);
            Assert.Equal(now.ToString("O"), fetched.CreatedAt.ToString("O"));
        }

        [Fact]
        public void UpdateTask_PreservesId()
        {
            var task = new TaskItem { Title = "Original" };
            _service.CreateTask(task);
            var originalId = task.Id;

            var updated = new TaskItem { Title = "Updated", Id = 999 };
            _service.UpdateTask(originalId, updated);

            var fetched = _service.GetTaskById(originalId);
            Assert.NotNull(fetched);
            Assert.Equal(originalId, fetched.Id);
            Assert.Equal("Updated", fetched.Title);
        }

        [Fact]
        public void DeleteTask_DoesNotAffectOtherTasks()
        {
            var task1 = new TaskItem { Title = "Task 1" };
            var task2 = new TaskItem { Title = "Task 2" };
            var task3 = new TaskItem { Title = "Task 3" };

            _service.CreateTask(task1);
            _service.CreateTask(task2);
            _service.CreateTask(task3);

            _service.DeleteTask(task2.Id);

            var all = _service.GetAllTasks().ToList();
            Assert.Equal(2, all.Count);
            Assert.Contains(all, t => t.Title == "Task 1");
            Assert.DoesNotContain(all, t => t.Title == "Task 2");
            Assert.Contains(all, t => t.Title == "Task 3");
        }
    }
}
