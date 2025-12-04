using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using DotnetApp.Models;

namespace DotnetApp.Services
{
    /// <summary>
    /// Provides a CSV-based implementation of the <see cref="ITaskService"/> interface.
    /// </summary>
    public class CsvTaskService : ITaskService
    {
        private readonly string _filePath;
        private readonly object _lock = new object();
        private int _nextId;

        /// <summary>
        /// Initializes a new instance of the <see cref="CsvTaskService"/> class.
        /// </summary>
        public CsvTaskService()
        {
            _filePath = Path.Combine(AppContext.BaseDirectory, "tasks.csv");
            if (!File.Exists(_filePath))
            {
                File.WriteAllText(_filePath, "Id,Title,Description,IsCompleted,Status,Priority,CreatedAt\n");
            }
            var tasks = ReadAll();
            _nextId = tasks.Any() ? tasks.Max(t => t.Id) : 0;
        }

        /// <summary>
        /// Reads all tasks from the CSV file.
        /// </summary>
        /// <returns>A list of all task items.</returns>
        private List<TaskItem> ReadAll()
        {
            var lines = File.ReadAllLines(_filePath);
            return lines
                .Skip(1)
                .Where(line => !string.IsNullOrWhiteSpace(line))
                .Select(line =>
                {
                    var parts = line.Split(',');
                    return new TaskItem
                    {
                        Id = int.Parse(parts[0]),
                        Title = parts[1],
                        Description = string.IsNullOrEmpty(parts[2]) ? null : parts[2],
                        IsCompleted = bool.Parse(parts[3]),
                        Status = parts[4],
                        Priority = int.Parse(parts[5]),
                        CreatedAt = DateTime.Parse(parts[6], null, DateTimeStyles.RoundtripKind)
                    };
                })
                .ToList();
        }

        /// <summary>
        /// Writes all tasks to the CSV file.
        /// </summary>
        /// <param name="tasks">The tasks to write.</param>
        private void WriteAll(IEnumerable<TaskItem> tasks)
        {
            var lines = new List<string> { "Id,Title,Description,IsCompleted,Status,Priority,CreatedAt" };
            lines.AddRange(tasks.Select(t =>
                string.Join(",",
                    t.Id,
                    Escape(t.Title),
                    Escape(t.Description),
                    t.IsCompleted,
                    t.Status,
                    t.Priority,
                    t.CreatedAt.ToString("O")
                )
            ));
            File.WriteAllLines(_filePath, lines);
        }

        /// <summary>
        /// Escapes a string value for CSV compatibility.
        /// </summary>
        /// <param name="value">The string value to escape.</param>
        /// <returns>The escaped string.</returns>
        private string Escape(string? value) => value?.Replace("\"", "\"\"") ?? string.Empty;

        /// <summary>
        /// Retrieves all tasks from the CSV file.
        /// </summary>
        /// <returns>A collection of all task items.</returns>
        public IEnumerable<TaskItem> GetAllTasks() => ReadAll();

        /// <summary>
        /// Retrieves a task by its unique identifier from the CSV file.
        /// </summary>
        /// <param name="id">The unique identifier of the task.</param>
        /// <returns>The task item if found; otherwise, null.</returns>
        public TaskItem? GetTaskById(int id) => ReadAll().FirstOrDefault(t => t.Id == id);

        /// <summary>
        /// Creates a new task and appends it to the CSV file.
        /// </summary>
        /// <param name="task">The task item to create.</param>
        public void CreateTask(TaskItem task)
        {
            lock (_lock)
            {
                task.Id = ++_nextId;
                var tasks = ReadAll();
                tasks.Add(task);
                WriteAll(tasks);
            }
        }

        /// <summary>
        /// Updates an existing task in the CSV file.
        /// </summary>
        /// <param name="id">The unique identifier of the task to update.</param>
        /// <param name="updatedTask">The updated task item.</param>
        /// <returns>True if the update was successful; otherwise, false.</returns>
        public bool UpdateTask(int id, TaskItem updatedTask)
        {
            lock (_lock)
            {
                var tasks = ReadAll();
                var existing = tasks.FirstOrDefault(t => t.Id == id);
                if (existing == null) return false;
                updatedTask.Id = id;
                tasks.Remove(existing);
                tasks.Add(updatedTask);
                WriteAll(tasks);
                return true;
            }
        }

        /// <summary>
        /// Deletes a task from the CSV file by its unique identifier.
        /// </summary>
        /// <param name="id">The unique identifier of the task to delete.</param>
        /// <returns>True if the deletion was successful; otherwise, false.</returns>
        public bool DeleteTask(int id)
        {
            lock (_lock)
            {
                var tasks = ReadAll();
                var removed = tasks.RemoveAll(t => t.Id == id) > 0;
                if (!removed) return false;
                WriteAll(tasks);
                return true;
            }
        }
    }
}
