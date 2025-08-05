namespace DotnetApp.Services
{
    using System.Collections.Concurrent;
    using DotnetApp.Models;

    /// <summary>
    /// Provides an in-memory implementation of the <see cref="ITaskService"/> interface.
    /// </summary>
    public class InMemoryTaskService : ITaskService
    {
        private readonly ConcurrentDictionary<int, TaskItem> _tasks = new();
        private int _nextId = 1;

        /// <summary>
        /// Retrieves all tasks stored in memory.
        /// </summary>
        /// <returns>A collection of all task items.</returns>
        public IEnumerable<TaskItem> GetAllTasks() => _tasks.Values;

        /// <summary>
        /// Retrieves a task by its unique identifier.
        /// </summary>
        /// <param name="id">The unique identifier of the task.</param>
        /// <returns>The task item if found; otherwise, null.</returns>
        public TaskItem? GetTaskById(int id) => _tasks.TryGetValue(id, out var task) ? task : null;

        /// <summary>
        /// Creates a new task and stores it in memory.
        /// </summary>
        /// <param name="task">The task item to create.</param>
        public void CreateTask(TaskItem task)
        {
            var id = System.Threading.Interlocked.Increment(ref _nextId);
            task.Id = id;
            _tasks[id] = task;
        }

        /// <summary>
        /// Updates an existing task in memory.
        /// </summary>
        /// <param name="id">The unique identifier of the task to update.</param>
        /// <param name="updatedTask">The updated task item.</param>
        /// <returns>True if the update was successful; otherwise, false.</returns>
        public bool UpdateTask(int id, TaskItem updatedTask)
        {
            if (!_tasks.ContainsKey(id)) return false;
            updatedTask.Id = id;
            _tasks[id] = updatedTask;
            return true;
        }

        /// <summary>
        /// Deletes a task from memory by its unique identifier.
        /// </summary>
        /// <param name="id">The unique identifier of the task to delete.</param>
        /// <returns>True if the deletion was successful; otherwise, false.</returns>
        public bool DeleteTask(int id) => _tasks.TryRemove(id, out _);
    }
}
