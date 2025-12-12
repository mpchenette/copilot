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
            int score = CalculatePriorityScore() + CalculateStatusScore();
            return Math.Max(0, score);
        }

        private int CalculatePriorityScore()
        {
            return Priority switch
            {
                <= 0 => 1,
                1 => Status == "pending" ? 13 : 10,
                2 => CalculatePriority2Score(),
                _ => 1
            };
        }

        private int CalculatePriority2Score()
        {
            if (Status != "in-progress" || IsCompleted)
                return 5;

            int score = 7;
            if ((DateTime.UtcNow - CreatedAt).TotalDays > 7)
                score += 3;
            return score;
        }

        private int CalculateStatusScore()
        {
            return Status.ToLower() switch
            {
                "pending" => CalculatePendingScore(),
                "in-progress" => CalculateInProgressScore(),
                _ => (!IsCompleted && Priority < 3) ? 3 : 0
            };
        }

        private int CalculatePendingScore()
        {
            if ((DateTime.UtcNow - CreatedAt).TotalDays <= 14)
                return 0;

            int currentScore = CalculatePriorityScore();
            int score = currentScore * 2;
            if (Priority < 3)
                score += 5;
            return score;
        }

        private int CalculateInProgressScore()
        {
            if (IsCompleted)
                return -5;

            int score = 0;
            foreach (var word in Title.Split(' '))
            {
                if (word.Length > 10)
                    score += 1;
            }
            return score;
        }
    }
}
