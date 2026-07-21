A function to calculate the longest common subsequence (LCS) of two strings.

// Function to find LCS using dynamic programming
int lcs(char X[], char Y[], int m, int n)
{
    // Create a table for storing results of sub-problems
    int dp[m + 1][n + 1];

    // Initialize the table with zeros
    for (int i = 0; i <= m; i++) {
        for (int j = 0; j <= n; j++) {
            dp[i][j] = 0;
        }
    }

    // Fill the table in a bottom-up manner
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (X[i - 1] == Y[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    // The LCS is stored in the last cell of the table
    return dp[m][n];
}

// Test the function with two example strings
int main()
{
    char str1[] = "abcde";
    char str2[] = "ace";
    int len1 = strlen(str1);
    int len2 = strlen(str2);
    int result = lcs(str1, str2, len1, len2);
    printf("The length of the LCS is: %d\n", result);

    return 0;
}