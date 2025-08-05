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
    }
}
