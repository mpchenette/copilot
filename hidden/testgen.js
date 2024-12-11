function getLinesDescription(numberOfLines) {
    if (numberOfLines == 0)
        return "There are no lines";
    else if (numberOfLines == 1)
        return "There is 1 line";
    else
        return "There are " + numberOfLines + " lines";
}
