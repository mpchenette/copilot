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
            int score = 0;

            score += CalculatePriorityScore();
            score += CalculateStatusScore(score);

            return Math.Max(0, score);
        }

        private int CalculatePriorityScore()
        {
            int score = 0;

            if (Priority <= 0)
            {
                score += 1;
            }
            else if (Priority == 1)
            {
                score += 10;
                if (Status == "pending")
                {
                    score += 3;
                }
            }
            else if (Priority == 2)
            {
                score += 5;
                if (Status == "in-progress" && !IsCompleted)
                {
                    score += 2;
                    if ((DateTime.UtcNow - CreatedAt).TotalDays > 7)
                    {
                        score += 3;
                    }
                }
            }
            else
            {
                score += 1;
            }

            return score;
        }

        private int CalculateStatusScore(int currentScore)
        {
            int score = 0;

            switch (Status.ToLower())
            {
                case "pending":
                    score += CalculatePendingScore(currentScore);
                    break;
                case "in-progress":
                    score += CalculateInProgressScore();
                    break;
                default:
                    if (!IsCompleted && Priority < 3)
                    {
                        score += 3;
                    }
                    break;
            }

            return score;
        }

        private int CalculatePendingScore(int currentScore)
        {
            int score = 0;

            if ((DateTime.UtcNow - CreatedAt).TotalDays > 14)
            {
                score += currentScore * 2;
                if (Priority < 3)
                {
                    score += 5;
                }
            }

            return score;
        }

        private int CalculateInProgressScore()
        {
            int score = 0;

            if (IsCompleted)
            {
                score -= 5;
            }
            else
            {
                foreach (var word in Title.Split(' '))
                {
                    if (word.Length > 10)
                    {
                        score += 1;
                    }
                }
            }

            return score;
        }
    }
}
