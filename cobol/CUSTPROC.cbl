       IDENTIFICATION DIVISION.
       PROGRAM-ID. CUSTPROC.
       AUTHOR. GITHUB-COPILOT.
       DATE-WRITTEN. 2025-03-28.
      
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT CUSTOMER-FILE
               ASSIGN TO 'CUSTFILE'
               ORGANIZATION IS SEQUENTIAL
               ACCESS MODE IS SEQUENTIAL
               FILE STATUS IS WS-FILE-STATUS.
           SELECT REPORT-FILE
               ASSIGN TO 'CUSTRPT'
               ORGANIZATION IS SEQUENTIAL
               ACCESS MODE IS SEQUENTIAL.
      
       DATA DIVISION.
       FILE SECTION.
       FD  CUSTOMER-FILE
           LABEL RECORDS ARE STANDARD.
       01  CUSTOMER-RECORD.
           05  CUST-ID             PIC X(6).
           05  CUST-NAME           PIC X(30).
           05  CUST-ADDRESS        PIC X(50).
           05  CUST-PHONE          PIC X(12).
           05  CUST-BALANCE        PIC 9(7)V99.
      
       FD  REPORT-FILE
           LABEL RECORDS ARE STANDARD.
       01  REPORT-LINE            PIC X(132).
      
       WORKING-STORAGE SECTION.
       01  WS-FILE-STATUS         PIC X(2).
       01  WS-EOF-FLAG           PIC X VALUE 'N'.
           88 END-OF-FILE        VALUE 'Y'.
      
       01  WS-COUNTERS.
           05  WS-READ-CTR       PIC 9(6) VALUE ZERO.
           05  WS-VALID-CTR      PIC 9(6) VALUE ZERO.
           05  WS-ERROR-CTR      PIC 9(6) VALUE ZERO.
      
       01  WS-HEADING-1.
           05  FILLER            PIC X(20) VALUE 'Customer Report     '.
           05  FILLER            PIC X(20) VALUE 'Date: '.
           05  WS-CURR-DATE      PIC X(10).
      
       01  WS-DETAIL-LINE.
           05  WS-DL-CUSTID      PIC X(6).
           05  FILLER            PIC X(2)  VALUE SPACES.
           05  WS-DL-NAME        PIC X(30).
           05  FILLER            PIC X(2)  VALUE SPACES.
           05  WS-DL-BALANCE     PIC $ZZZ,ZZ9.99.
      
       PROCEDURE DIVISION.
       0100-MAIN-PROCESS.
           PERFORM 0200-INIT-ROUTINE
           PERFORM 0300-PROCESS-RECORDS UNTIL END-OF-FILE
           PERFORM 0900-CLOSE-ROUTINE
           STOP RUN.
      
       0200-INIT-ROUTINE.
           OPEN INPUT  CUSTOMER-FILE
                OUTPUT REPORT-FILE
           IF WS-FILE-STATUS NOT = '00'
               DISPLAY 'Error opening files. Status: ' WS-FILE-STATUS
               MOVE 'Y' TO WS-EOF-FLAG
           END-IF
           PERFORM 0250-WRITE-HEADERS.
      
       0250-WRITE-HEADERS.
           MOVE FUNCTION CURRENT-DATE(1:10) TO WS-CURR-DATE
           WRITE REPORT-LINE FROM WS-HEADING-1
           WRITE REPORT-LINE FROM SPACES.
      
       0300-PROCESS-RECORDS.
           READ CUSTOMER-FILE
               AT END
                   MOVE 'Y' TO WS-EOF-FLAG
               NOT AT END
                   ADD 1 TO WS-READ-CTR
                   PERFORM 0400-VALIDATE-RECORD
           END-READ.
      
       0400-VALIDATE-RECORD.
           IF CUST-BALANCE > 0
               PERFORM 0500-FORMAT-DETAIL
               ADD 1 TO WS-VALID-CTR
           ELSE
               ADD 1 TO WS-ERROR-CTR
           END-IF.
      
       0500-FORMAT-DETAIL.
           MOVE CUST-ID TO WS-DL-CUSTID
           MOVE CUST-NAME TO WS-DL-NAME
           MOVE CUST-BALANCE TO WS-DL-BALANCE
           WRITE REPORT-LINE FROM WS-DETAIL-LINE.
      
       0900-CLOSE-ROUTINE.
           WRITE REPORT-LINE FROM SPACES
           MOVE 'Total Records Read:   ' TO REPORT-LINE
           MOVE WS-READ-CTR TO REPORT-LINE(25:6)
           WRITE REPORT-LINE
           MOVE 'Valid Records:        ' TO REPORT-LINE
           MOVE WS-VALID-CTR TO REPORT-LINE(25:6)
           WRITE REPORT-LINE
           MOVE 'Error Records:        ' TO REPORT-LINE
           MOVE WS-ERROR-CTR TO REPORT-LINE(25:6)
           WRITE REPORT-LINE
           CLOSE CUSTOMER-FILE
                 REPORT-FILE.