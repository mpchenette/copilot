namespace DotnetApp.Services
{
    using DotnetApp.Models;
    using System.Collections.Generic;

    /// <summary>
    /// Defines the contract for task management services.
    /// </summary>
    public interface ITaskService
    {
        /// <summary>
        /// Retrieves all tasks.
        /// </summary>
        /// <returns>A collection of all task items.</returns>
        IEnumerable<TaskItem> GetAllTasks();

        /// <summary>
        /// Retrieves a task by its unique identifier.
        /// </summary>
        /// <param name="id">The unique identifier of the task.</param>
        /// <returns>The task item if found; otherwise, null.</returns>
        TaskItem? GetTaskById(int id);

        /// <summary>
        /// Creates a new task.
        /// </summary>
        /// <param name="task">The task item to create.</param>
        void CreateTask(TaskItem task);

        /// <summary>
        /// Updates an existing task.
        /// </summary>
        /// <param name="id">The unique identifier of the task to update.</param>
        /// <param name="updatedTask">The updated task item.</param>
        /// <returns>True if the update was successful; otherwise, false.</returns>
        bool UpdateTask(int id, TaskItem updatedTask);

        /// <summary>
        /// Deletes a task by its unique identifier.
        /// </summary>
        /// <param name="id">The unique identifier of the task to delete.</param>
        /// <returns>True if the deletion was successful; otherwise, false.</returns>
        bool DeleteTask(int id);
    }
}
