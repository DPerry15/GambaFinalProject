namespace Gamble.Components.Models
{
    public class CreditsData
    {

        public int CreditsCount { get; set; } = 0;

        public void IncrementCount()
        {
            CreditsCount++;

        }
    }
}
