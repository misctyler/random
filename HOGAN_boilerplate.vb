Option Explicit
 
Dim sys As BZWHLLLib.WhllObj
Dim sess As BZWHLLLib.session
Dim screen As BZWHLLLib.screen
Dim oia As BZWHLLLib.oia
 
Sub Main()
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Set sys = New BZWHLLLib.WhllObj
    Set sess = sys.ActiveSession
    Set screen = sess.screen
    Set oia = screen.oia
   
    GetHoganData
 
    Set sys = Nothing
    Set sess = Nothing
    Set screen = Nothing
    Set oia = Nothing
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    ThisWorkbook.Save
End Sub

Function GetHoganData()
    Dim wsMain As Worksheet
    Dim loan As Range
    Dim bor_ As String
    Dim loans As Range
    Set wsMain = ThisWorkbook.Worksheets("MAIN")
    Set loans = wsMain.Range("LOANS")
    For Each loan In loans
        If loan.Interior.ColorIndex <> 4 Then
 
        loan.Interior.ColorIndex = 4
        End If
       
    Next
End Function
 
'Convert Hogan date format YYY/MM/DD
Function hogDt(str As String) As String
    If str = "" Then
        hogDt = str
    Else
        hogDt = Mid(str, 4, 2) & "/" & Right(str, 2) & "/" & Left(str, 2)
    End If
End Function
 
Function Clear()
    screen.SendKeys "<clear>"
    WaitForInputReady
End Function
 
Function SetCursor(ByVal ROW As Integer, col As Integer)
    screen.MoveTo ROW, col
    screen.WaitForCursor ROW, col
End Function
 
Function GetText(ROW As Integer, col As Integer, length As Long) As String
    GetText = Trim(screen.GetString(ROW, col, length))
End Function
 
Function SendText(ByVal text As String)
    screen.SendKeys text
End Function
 
Function Enter()
    screen.SendKeys "<Enter>"
    WaitForInputReady
End Function
 
Function EraseEOF()
    screen.SendKeys "<EraseEOF>"
End Function
 
Function TabOver()
    screen.SendKeys "<Tab>"
End Function
 
Function Home()
    screen.SendKeys "<Home>"
End Function
 
Function F1()
    screen.SendKeys "<Pf1>"
    WaitForInputReady
End Function
 
Function F2()
    screen.SendKeys "<Pf2>"
    WaitForInputReady
End Function
 
Function F3()
    screen.SendKeys "<Pf3>"
    WaitForInputReady
End Function
 
Function F4()
    screen.SendKeys "<Pf4>"
    WaitForInputReady
End Function
 
Function F5()
    screen.SendKeys "<Pf5>"
    WaitForInputReady
End Function
 
Function F6()
    screen.SendKeys "<Pf6>"
    WaitForInputReady
End Function
 
Function F7()
    screen.SendKeys "<Pf7>"
    WaitForInputReady
End Function
 
Function F8()
    screen.SendKeys "<Pf8>"
    WaitForInputReady
End Function
 
Function F9()
    screen.SendKeys "<Pf9>"
    WaitForInputReady
End Function
 
Function F10()
    screen.SendKeys "<Pf10>"
    WaitForInputReady
End Function
 
Function F11()
    screen.SendKeys "<Pf11>"
    WaitForInputReady
End Function
 
Function F12()
    screen.SendKeys "<Pf12>"
    WaitForInputReady
End Function
 
Function F13()
    screen.SendKeys "<Pf13>"
    WaitForInputReady
End Function
 
Function F14()
    screen.SendKeys "<Pf14>"
    WaitForInputReady
End Function
 
Function F15()
    screen.SendKeys "<Pf15>"
    WaitForInputReady
End Function
 
Function F16()
    screen.SendKeys "<Pf16>"
    WaitForInputReady
End Function
 
Function F17()
    screen.SendKeys "<Pf17>"
    WaitForInputReady
End Function
 
Function F18()
    screen.SendKeys "<Pf18>"
    WaitForInputReady
End Function
 
Function F19()
    screen.SendKeys "<Pf19>"
    WaitForInputReady
End Function
 
Function F20()
    screen.SendKeys "<Pf20>"
    WaitForInputReady
End Function
 
Function F21()
    screen.SendKeys "<Pf11>"
    WaitForInputReady
End Function
 
Function F22()
    screen.SendKeys "<Pf22>"
    WaitForInputReady
End Function
 
Function F23()
    screen.SendKeys "<Pf23>"
    WaitForInputReady
End Function
 
Function F24()
    screen.SendKeys "<Pf24>"
    WaitForInputReady
End Function
 
Function WaitForInputReady()
    Do Until oia.XStatus <> 5
        screen.WaitHostQuiet (750)
    Loop
End Function
