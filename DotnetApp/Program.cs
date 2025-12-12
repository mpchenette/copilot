using DotnetApp.Services;
using DotnetApp.Models;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddSingleton<ITaskService, CsvTaskService>();

var app = builder.Build();

// Serve UI from wwwroot instead of external templates folder
app.UseDefaultFiles();
app.UseStaticFiles();

// Replace simple GET /tasks with optional status query
app.MapGet("/tasks", (string? status, ITaskService service) =>
{
    var tasks = service.GetAllTasks();
    if (!string.IsNullOrEmpty(status))
        tasks = tasks.Where(t => t.Status == status);
    return Results.Ok(tasks);
});
app.MapGet("/tasks/{id}", (int id, ITaskService service) =>
    service.GetTaskById(id) is TaskItem task ? Results.Ok(task) : Results.NotFound());
app.MapPost("/tasks", (TaskItem task, ITaskService service) =>
{
    service.CreateTask(task);
    return Results.Created($"/tasks/{task.Id}", task);
});
// Update returns the modified task JSON instead of NoContent
app.MapPut("/tasks/{id}", (int id, TaskItem updatedTask, ITaskService service) =>
{
    updatedTask.Id = id;
    return service.UpdateTask(id, updatedTask)
        ? Results.Ok(updatedTask)
        : Results.NotFound();
});
app.MapDelete("/tasks/{id}", (int id, ITaskService service) =>
    service.DeleteTask(id) ? Results.NoContent() : Results.NotFound());

await app.RunAsync();
