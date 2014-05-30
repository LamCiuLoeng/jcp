# -*- coding: utf-8 -*-
import os, traceback, logging, datetime
import win32com.client
import pythoncom

from win32com.client import DispatchEx
from common import *

__all__ = ["JCPExcel", "HangTagProductionExcel", "RFIDExcel"]

class ExcelBasicGenerator:
    def __init__(self, templatePath = None, destinationPath = None, overwritten = True):
        #solve the problem when create the excel at second time ,the exception is occur.
        pythoncom.CoInitialize()

        self.excelObj = DispatchEx('Excel.Application')
#        self.excelObj.Visible = False

        if templatePath and os.path.exists(templatePath):
            self.workBook = self.excelObj.Workbooks.open(templatePath)
        else:
            self.workBook = self.excelObj.Workbooks.Add()

        self.destinationPath = os.path.normpath(destinationPath) if destinationPath else None
        self.overwritten = overwritten

    def inputData(self): pass

    def outputData(self):
        try:
            if not self.destinationPath : pass
            elif os.path.exists(self.destinationPath):
                if self.overwritten:
                    os.remove(self.destinationPath)
                    self.excelObj.ActiveWorkbook.SaveAs(self.destinationPath)
            else:
                self.excelObj.ActiveWorkbook.SaveAs(self.destinationPath)
        except:
            file = open('log.txt', 'a')
            traceback.print_exc(None, file)
            file.close()
#            traceback.print_exc()
        finally:
            try:
                self.workBook.Close(SaveChanges = 0)
            except:
                traceback.print_exc()

    def clearData(self):
        try:
            if hasattr(self, "workBook"): self.workBook.Close(SaveChanges = 0)
        except:
            file = open('log.txt', 'a')
            traceback.print_exc(None, file)
            file.close()
#            traceback.print_exc()

class JCPExcel(ExcelBasicGenerator):
    def inputData(self, additionInfo = [], header = [], data = []):
        excelSheet = self.workBook.Sheets(1)
        excelSheet.Cells(4, 1).Value = "Export Time : %s" % datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        infoStartRow = 5
        infoStartCol = 1

        for oneCriteria in additionInfo:
            excelSheet.Cells(infoStartRow, infoStartCol).Value = oneCriteria
            infoStartRow += 1

        if not data: data = [("",), ]

        row = len(data)
        col = len(data[0])
        startRow = 16
        startCol = 1

        excelSheet.Range("A%d:%s%d" % (startRow, number2alphabet(col), startRow + row - 1)).Value = data
        excelSheet.Columns("A:AZ").EntireColumn.AutoFit()

class HangTagProductionExcel(ExcelBasicGenerator):
    def inputData(self, extra_info = [], header = [], data = []):
        excelSheet = self.workBook.Sheets(1)
        
        infoStartRow = 5
        infoStartCol = 1

        if not data: data = [("",), ]

        row = len(data)
        col = len(data[0])
        startRow = 19
        startCol = 1
        
        if extra_info[0] is not None:
            if len(extra_info) == 4:
                excelSheet.Range("F4").Value = ''.join(['Item Code: ', extra_info[0].item_code])
                excelSheet.Name = 'HangTag'
            elif len(extra_info) == 5:
                excelSheet.Range("F4").Value = ''.join(['Item Code: ', extra_info[0].item_code])
                excelSheet.Name = 'Sticker'
        
        excelSheet.Range("billCompany").Value = header.orders[0].billCompany
        excelSheet.Range("billAddress").Value = header.orders[0].billAddress
        excelSheet.Range("billAttn").Value = header.orders[0].billAttn
        excelSheet.Range("billTel").Value = header.orders[0].billTel
        excelSheet.Range("billFax").Value = header.orders[0].billFax
        excelSheet.Range("billEmail").Value = header.orders[0].billEmail
        excelSheet.Range("shipCompany").Value = header.orders[0].shipCompany
        excelSheet.Range("shipAddress").Value = header.orders[0].shipAddress
        excelSheet.Range("shipAttn").Value = header.orders[0].shipAttn
        excelSheet.Range("shipTel").Value = header.orders[0].shipTel
        excelSheet.Range("shipFax").Value = header.orders[0].shipFax
        excelSheet.Range("shipEmail").Value = header.orders[0].shipEmail
        excelSheet.Range("PONumber").Value = header.poNo
        excelSheet.Range("CustomPO").Value = header.orders[0].customerPO
        
        if header.orders[0].supplierNO and header.orders[0].supplierNO.startswith('7'):
            excelSheet.Range("supplierNO").value = '19963-8'
        else:
            excelSheet.Range("supplierNO").value = header.orders[0].supplierNO
        
        excelSheet.Range("ShipInstruction").Value = header.orders[0].shipInstruction
        excelSheet.Range("TotalQty").Value = extra_info[-1]
        excelSheet.Range("ItemCodes").Value = header.orders[0].cust_item_codes
        excelSheet.Range("Remark").Value = header.remark
        excelSheet.Range("COO").Value = extra_info[-2].countryName
        
        excelSheet.Range("A%d:%s%d" % (startRow - 1, number2alphabet(col), startRow - 1)).Value = extra_info[1]
        excelSheet.Range("A%d:%s%d" % (startRow - 1, number2alphabet(col), startRow - 1)).Font.Name = "Trebuchet MS"
        excelSheet.Range("A%d:%s%d" % (startRow - 1, number2alphabet(col), startRow - 1)).Font.Size = 10
        excelSheet.Range("A%d:%s%d" % (startRow - 1, number2alphabet(col), startRow - 1)).Font.Bold = True
        excelSheet.Range("A%d:%s%d" % (startRow - 1, number2alphabet(col), startRow - 1)).Font.ColorIndex = 0
        excelSheet.Range("A%d:%s%d" % (startRow - 1, number2alphabet(col), startRow - 1)).Interior.ColorIndex = 33
        excelSheet.Range("%s%d:%s%d" % (number2alphabet(15), startRow - 1, number2alphabet(15 + col - len(extra_info[1]) + 1), startRow - 1)).ColumnWidth = 15
        
        excelSheet.Range("A%d:%s%d" % (startRow, number2alphabet(col), startRow + row - 1)).Value = data
        
#        for qty_row in range(startRow, startRow + row):
#            if isinstance(excelSheet.Cells(qty_row, len(data[0]) - 1).Value, int):
#                excelSheet.Cells(qty_row, len(data[0]) - 1).NumberFormatLocal = "0_"
#            elif isinstance(excelSheet.Cells(qty_row, len(data[0]) - 1).Value, float):
#                excelSheet.Cells(qty_row, len(data[0]) - 1).NumberFormatLocal = "2_"
        
#        excelSheet.Columns("A:AZ").EntireColumn.AutoFit()

class RFIDExcel(ExcelBasicGenerator):
    def inputData(self,data=[],qty=0):
        excelSheet = self.workBook.Sheets(1)
        excelSheet2 = self.workBook.Sheets(2)
        excelSheet3 = self.workBook.Sheets(3)
        excelSheet4 = self.workBook.Sheets(4)
        excelSheet5 = self.workBook.Sheets(5)
        if not data:
            data = [("",),]

        startRow = 2
        row = len(data)
        col = len(data[0])

        if row <= 50000:
            excelSheet.Range("A%d:%s%d" %( startRow, number2alphabet(col)  ,startRow+row-1 )).Value = data
        elif row > 50000 and row <= 100000:
            excelSheet.Range("A%d:%s%d" %( startRow, number2alphabet(col)  ,startRow+50000-1 )).Value = data[0:50000]
            excelSheet2.Range("A%d:%s%d" %( startRow, number2alphabet(col)  ,startRow+row-50000-1 )).Value = data[50000:]
        elif row > 100000 and row <=150000:
            excelSheet.Range("A%d:%s%d" %( startRow, number2alphabet(col)  ,startRow+50000-1 )).Value = data[0:50000]
            excelSheet2.Range("A%d:%s%d" %( startRow, number2alphabet(col)  ,startRow+50000-1 )).Value = data[50000:100000]
            excelSheet3.Range("A%d:%s%d" %( startRow, number2alphabet(col)  ,startRow+row-100000-1 )).Value = data[100000:]
        elif row >150000 and row <=200000:
            excelSheet.Range("A%d:%s%d" %( startRow, number2alphabet(col)  ,startRow+50000-1 )).Value = data[0:50000]
            excelSheet2.Range("A%d:%s%d" %( startRow, number2alphabet(col)  ,startRow+50000-1 )).Value = data[50000:100000]
            excelSheet3.Range("A%d:%s%d" %( startRow, number2alphabet(col)  ,startRow+50000-1 )).Value = data[100000:150000]
            excelSheet4.Range("A%d:%s%d" %( startRow, number2alphabet(col)  ,startRow+row-150000-1 )).Value = data[150000:]
        elif row >200000 and row <= 250000:
            excelSheet.Range("A%d:%s%d" %( startRow, number2alphabet(col)  ,startRow+50000-1 )).Value = data[0:50000]
            excelSheet2.Range("A%d:%s%d" %( startRow, number2alphabet(col)  ,startRow+50000-1 )).Value = data[50000:100000]
            excelSheet3.Range("A%d:%s%d" %( startRow, number2alphabet(col)  ,startRow+50000-1 )).Value = data[100000:150000]
            excelSheet4.Range("A%d:%s%d" %( startRow, number2alphabet(col)  ,startRow+50000-1 )).Value = data[150000:200000]
            excelSheet5.Range("A%d:%s%d" %( startRow, number2alphabet(col)  ,startRow+row-200000-1 )).Value = data[200000:]
        #excelSheet.Range("A%d:%s%d" %( startRow, number2alphabet(col), startRow+row-1 )).Value = data
