using System.Text.Json.Serialization;

namespace DotnetApp.Models
{
    public class TaskItem
    {
        public int Id { get; set; }
        public string Title { get; set; } = default!;
        public string? Description { get; set; }
        public bool IsCompleted { get; set; }

        [JsonPropertyName("priority")]
        public int Priority { get; set; } = 3;

        [JsonPropertyName("status")]
        public string Status { get; set; } = "pending";

        [JsonPropertyName("created_at")]
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        public int CalculateTaskScore()
        {
            int priorityScore = CalculatePriorityScore();
            int statusScore = CalculateStatusScore(priorityScore);

            return Math.Max(0, priorityScore + statusScore);
        }

        private int CalculatePriorityScore()
        {
            if (Priority <= 0) return 1;
            if (Priority == 1) return CalculateHighPriorityScore();
            if (Priority == 2) return CalculateMediumPriorityScore();
            return 1;
        }

        private int CalculateHighPriorityScore()
        {
            int score = 10;
            if (Status == "pending") score += 3;
            return score;
        }

        private int CalculateMediumPriorityScore()
        {
            int score = 5;
            if (Status == "in-progress" && !IsCompleted)
            {
                score += 2;
                if ((DateTime.UtcNow - CreatedAt).TotalDays > 7) score += 3;
            }
            return score;
        }

        private int CalculateStatusScore(int priorityScore)
        {
            return Status.ToLower() switch
            {
                "pending" => CalculatePendingScore(priorityScore),
                "in-progress" => CalculateInProgressScore(),
                _ => (!IsCompleted && Priority < 3) ? 3 : 0
            };
        }

        private int CalculatePendingScore(int priorityScore)
        {
            if ((DateTime.UtcNow - CreatedAt).TotalDays <= 14) return 0;
            
            int score = priorityScore * 2;
            if (Priority < 3) score += 5;
            return score;
        }

        private int CalculateInProgressScore()
        {
            if (IsCompleted) return -5;

            int score = 0;
            foreach (var word in Title.Split(' '))
            {
                if (word.Length > 10) score += 1;
            }
            return score;
        }
    }
}
