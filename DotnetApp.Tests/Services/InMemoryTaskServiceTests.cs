using System.Linq;
using DotnetApp.Models;
using DotnetApp.Services;
using Xunit;

namespace DotnetApp.Tests.Services
{
    public class InMemoryTaskServiceTests
    {
        [Fact]
        public void CreateTask_AssignsIdAndStoresTask()
        {
            var service = new InMemoryTaskService();
            var task = new TaskItem { Title = "Test Task" };

            service.CreateTask(task);

            Assert.NotEqual(0, task.Id);
            var all = service.GetAllTasks().ToList();
            Assert.Contains(all, t => t.Id == task.Id && t.Title == "Test Task");
        }

        [Fact]
        public void GetTaskById_ReturnsCorrectTaskOrNull()
        {
            var service = new InMemoryTaskService();
            var task = new TaskItem { Title = "GetById" };
            service.CreateTask(task);
            var id = task.Id;

            var found = service.GetTaskById(id);
            Assert.NotNull(found);
            Assert.Equal("GetById", found.Title);

            var missing = service.GetTaskById(id + 999);
            Assert.Null(missing);
        }

        [Fact]
        public void UpdateTask_NonExisting_ReturnsFalse()
        {
            var service = new InMemoryTaskService();
            var updated = new TaskItem { Title = "Nope" };

            var result = service.UpdateTask(999, updated);
            Assert.False(result);
        }

        [Fact]
        public void UpdateTask_Existing_ReturnsTrueAndUpdates()
        {
            var service = new InMemoryTaskService();
            var task = new TaskItem { Title = "Original" };
            service.CreateTask(task);
            var id = task.Id;

            var updated = new TaskItem { Title = "Updated" };
            var result = service.UpdateTask(id, updated);

            Assert.True(result);
            Assert.Equal(id, updated.Id);
            var fetched = service.GetTaskById(id);
            Assert.Equal("Updated", fetched.Title);
        }

        [Fact]
        public void DeleteTask_ReturnsTrueOnceAndRemoves()
        {
            var service = new InMemoryTaskService();
            var task = new TaskItem { Title = "ToDelete" };
            service.CreateTask(task);
            var id = task.Id;

            var first = service.DeleteTask(id);
            var second = service.DeleteTask(id);

            Assert.True(first);
            Assert.False(second);
            Assert.Null(service.GetTaskById(id));
        }

        [Fact]
        public void GetAllTasks_Empty_ReturnsEmpty()
        {
            var service = new InMemoryTaskService();
            var all = service.GetAllTasks().ToList();
            Assert.Empty(all);
        }

        [Fact]
        public void CreateTask_SequentialIds()
        {
            var service = new InMemoryTaskService();
            var t1 = new TaskItem { Title = "First" };
            service.CreateTask(t1);
            var t2 = new TaskItem { Title = "Second" };
            service.CreateTask(t2);

            Assert.Equal(t1.Id + 1, t2.Id);
        }

        [Fact]
        public void GetAllTasks_ReturnsMultipleTasks()
        {
            var service = new InMemoryTaskService();
            var task1 = new TaskItem { Title = "Task 1" };
            var task2 = new TaskItem { Title = "Task 2" };
            var task3 = new TaskItem { Title = "Task 3" };

            service.CreateTask(task1);
            service.CreateTask(task2);
            service.CreateTask(task3);

            var all = service.GetAllTasks().ToList();
            Assert.Equal(3, all.Count);
            Assert.Contains(all, t => t.Title == "Task 1");
            Assert.Contains(all, t => t.Title == "Task 2");
            Assert.Contains(all, t => t.Title == "Task 3");
        }

        [Fact]
        public void UpdateTask_PreservesId()
        {
            var service = new InMemoryTaskService();
            var task = new TaskItem { Title = "Original" };
            service.CreateTask(task);
            var originalId = task.Id;

            var updated = new TaskItem { Title = "Updated", Id = 999 };
            service.UpdateTask(originalId, updated);

            var fetched = service.GetTaskById(originalId);
            Assert.NotNull(fetched);
            Assert.Equal(originalId, fetched.Id);
            Assert.Equal("Updated", fetched.Title);
        }

        [Fact]
        public void UpdateTask_UpdatesAllProperties()
        {
            var service = new InMemoryTaskService();
            var task = new TaskItem 
            { 
                Title = "Original",
                Description = "Original Description",
                Status = "pending",
                Priority = 3,
                IsCompleted = false
            };
            service.CreateTask(task);
            var id = task.Id;

            var updated = new TaskItem 
            { 
                Title = "Updated Title",
                Description = "Updated Description",
                Status = "completed",
                Priority = 1,
                IsCompleted = true
            };
            service.UpdateTask(id, updated);

            var fetched = service.GetTaskById(id);
            Assert.NotNull(fetched);
            Assert.Equal("Updated Title", fetched.Title);
            Assert.Equal("Updated Description", fetched.Description);
            Assert.Equal("completed", fetched.Status);
            Assert.Equal(1, fetched.Priority);
            Assert.True(fetched.IsCompleted);
        }

        [Fact]
        public void DeleteTask_DoesNotAffectOtherTasks()
        {
            var service = new InMemoryTaskService();
            var task1 = new TaskItem { Title = "Task 1" };
            var task2 = new TaskItem { Title = "Task 2" };
            var task3 = new TaskItem { Title = "Task 3" };

            service.CreateTask(task1);
            service.CreateTask(task2);
            service.CreateTask(task3);

            service.DeleteTask(task2.Id);

            var all = service.GetAllTasks().ToList();
            Assert.Equal(2, all.Count);
            Assert.Contains(all, t => t.Title == "Task 1");
            Assert.DoesNotContain(all, t => t.Title == "Task 2");
            Assert.Contains(all, t => t.Title == "Task 3");
        }

        [Fact]
        public void CreateTask_WithNullDescription_Works()
        {
            var service = new InMemoryTaskService();
            var task = new TaskItem 
            { 
                Title = "No Description",
                Description = null
            };
            service.CreateTask(task);

            var fetched = service.GetTaskById(task.Id);
            Assert.NotNull(fetched);
            Assert.Null(fetched.Description);
        }
    }
}
