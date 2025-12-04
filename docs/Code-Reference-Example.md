# Code Citations

## License: unknown
https://github.com/sli7236/QuickSort/tree/c7e584891b75fd1ca0f01c7cd308b09c96fad008/src/com/company/quickSort.java

```
static int Partition(int[] arr, int left, int right)
{
    int pivot = arr[right];
    int i = left - 1;
    for (int j = left; j < right; j++)
    {
        if (arr[j] <=
```


## License: unknown
https://github.com/petriucmihai/Interview-Problems/tree/8d5bb453f25bf130aca34682494aa2435222474c/InterviewProblems/SearchingAndSorting/SortingAlgorithms/QuickSort.cs

```
private static int Partition(int[] arr, int left, int right)
{
    int pivot = arr[right];
    int i = left - 1;
    for (int j = left; j < right; j++)
    {
        if (arr[j] <
```


## License: MIT
https://github.com/CodeMazeBlog/CodeMazeGuides/tree/e8a3b277ba7b5c70147a3f82e64477d9d88cc0b5/dotnet-client-libraries/BenchmarkDotNet-MemoryDiagnoser-Attribute/BenchmarkDotNet-MemoryDiagnoser-Attribute/Sort.cs

```
QuickSort(int[] arr, int left, int right)
{
    if (left < right)
    {
        int pivotIndex = Partition(arr, left, right);
        QuickSort(arr, left, pivotIndex - 1);
        QuickSort(arr, pivotIndex + 1, right);
```


## License: unknown
https://github.com/giangpham712/dsa-csharp/tree/e6aaf295082d34b376b3e8ac0929b05005508d6b/src/Algorithms/Sorting/QuickSort.cs

```
arr[i], arr[j]) = (arr[j], arr[i]);
        }
    }
    (arr[i + 1], arr[right]) = (arr[right], arr[i + 1]);
    return i
```


## License: unknown
https://github.com/krmphasis/QuickSort1/tree/aeefa44f535beee0a50e330c0e882fc530a7255d/QuickSortLogic.cs

```
right)
{
    if (left < right)
    {
        int pivotIndex = Partition(arr, left, right);
        QuickSort(arr, left, pivotIndex - 1);
        QuickSort(arr, pivotIndex + 1, right);
    }
}

private static int Partition(int[] arr
```

