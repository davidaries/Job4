# Job4
Job 4.docx

Task -2: (Dan) create updated pdata and adat tables so the UI can retrieve the data it needs.

Task -1: (Dan) review the UI spec in the protocol table to make sure it still works

Task 0:
We continue with Manual, but let’s keep an eye on being able to do Auto and Mixed
The simulation can run in three modes:
-	Manual: staff screens pop up and we need to manually fill and submit (as currently)
-	Auto (the simulation delays a period of time** and then auto-fills*** and then submits
-	Mixed mode: some staffers run on auto, others need to be entered manually

Task 1:
Put in place something in the simulation environment with “timer” and a loop counter function.
-	e.g., something like current_time equals start_time + (#_loops * increment_time)

Task 2:
The simulation environment:
-	Put the Protocol Engine (PE) within that
-	Note 1: I don’t see PE itself directly interacting with the simulation process/clock. It only runs off pe_in.
-	Note 2: the current implementation is doing one weird little thing that will probably go away on its own when this gets re-written

Task 3:
Staffer UI:
-	Add to their task_view the extra elements in pe_out

Task 4: self-updating views of:
-	pe_outs – current and log
-	pe_waits – current and log
-	pe_ins – current and log
-	pdata
Note: by current and log, show what is currently in each, and a log of what has been in each. (those could be in the same view, for instance, with current on top, and then the log underneath). Because (I don’t think I said this, but it happens in the code, when a user acts on pe_out, it comes off the pe_outs table, and when they return a pe_in, the PE finds its match in pe_waits, and take both (the pe_in and the pe_wait) out of their respective tables. 

Task 5:
The simulation environment:
-	Staff signing on to work – with a “device”   (simple login button on UI)

Task 6: We need better approaches to the intake protocol seeding process of lines 19-35. Two ideas (these need more thought before doing:
1.	Have persons randomly show up (on a time basis) and randomly pulling a first and last name from a list. And everyone gets a chief complaint of fever or cough.
2.	The initiate button approach
Add to a staffers task_view screen add an “Initiate” button. 
o	For the receptionist, when they push that button, it gives them a chance to enter person (currently just as a number), and it writes to pe_ins per lines 32-33 in main.py of PEv1.

** Some notes on the time delay. 
  When staff members are in auto mode, the time delay might depend depending on as many as five things:
a)	the task to be done (it takes longer for the provider to see a person than for the receptionist to gather their initial few details)
b)	the staffer's role (a junior lab technician takes longer than a lab supervisor to do the same lab task)
c)	the staffer themself (Provider Jake is just plain faster than Provider John in seeing persons)
d)	a bit of randomness (random between)
e)	and if the staff member is currently running behind, the time delay can't start until they have finished their previous task (Provider Jake can't see Person Steve in the usual time if he is still seeing Person Sam).
  But for now, let’s just do a and d.

*** On auto-filling and filling data:
-	Deal with value type, and check for proper format if number
-	Check for the range if number (upper, lower)
-	And have a stock of values to use for auto-filling (random.sample is py function I think)


