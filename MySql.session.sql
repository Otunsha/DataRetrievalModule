-- Calculate the size of one row
DECLARE @RowSize INT;
SET @RowSize = 
    (4 +  -- ID INT column size (4 bytes)
    4 +  -- PID INT column size (4 bytes)
    4 +  -- PPID INT column size (4 bytes)
    (LEN('Sample Text') * 2) +  -- NAME VARCHAR column size (variable-length)
    4 +  -- CPU_PERCENT FLOAT column size (4 bytes)
    4 +  -- WSET FLOAT column size (4 bytes)
    4 +  -- PEAK_WSET FLOAT column size (4 bytes)
    4 +  -- PFILES FLOAT column size (4 bytes)
    4 +  -- PEAK_PFILES FLOAT column size (4 bytes)
    4 +  -- NUM_PFAULTS FLOAT column size (4 bytes)
    4 +  -- PRIVATE FLOAT column size (4 bytes)
    (LEN('Sample Text') * 2) +  -- STATUS VARCHAR column size (variable-length)
    8 +  -- CREATE_TIME DATETIME column size (8 bytes)
    8);  -- TIME_STAMP DATETIME column size (8 bytes)

-- Print the estimated row size in bytes
PRINT 'Estimated Row Size: ' + CAST(@RowSize AS VARCHAR) + ' bytes';
