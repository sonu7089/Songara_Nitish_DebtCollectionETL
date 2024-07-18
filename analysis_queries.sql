a. What is the average loan amount for borrowers who are more than 5 days past due?
Query-> select ROUND(AVG(`Loan Amount`), 2) as 'Average Amount' from Repayments 
	where `Days Left to Pay Current EMI` > 5 and `Delayed Payment` = 'Yes'

b. Who are the top 10 borrowers with the highest outstanding balance?
Query-> Select `Id`, ((`EMI` * `Loan Term`) - (`EMI` * COUNT(*))) as 'Outstanding Amount' 
	from Repayments
	GROUP by `Id`
	ORDER BY ((`EMI` * `Loan Term`) - (`EMI` * COUNT(*))) DESC
	LIMIT 10


c  List of all borrowers with good repayment history
Query-> with CTE as (
	select `Name`, `Repayment Date` as Date, Lag(`Repayment Date`) OVER (PARTITION BY `Id` ORDER BY `Repayment 	Date`) as LagDate from Repayments 
	where `Delayed Payment` = 'No'
	), CTE2 as (
		select `Name`, 
		CASE 
			WHEN LagDate is NULL then 45
			WHEN julianday(Date) - julianday(LagDate) <= 45 THEN 45
			ELSE 50
		END AS Diff 
		FROM CTE
	)

	select `Name` from CTE2 
	GROUP BY `Name`
	HAVING AVG(Diff) = 45

d  Brief analysis wrt loan type
	-> Avg Amount for Different Loan Types:
		Select `Load Type`,Round(AVG(`Loan Amount`),2) as AverageLoanAmount from Repayments 
		GROUP BY `Load Type`
	-> Avg Loan Term of Different Loan Types:
		Select `Load Type`,Round(AVG(`Loan Term`),2) as AverageLoanAmount from Repayments 
		GROUP BY `Load Type`
	