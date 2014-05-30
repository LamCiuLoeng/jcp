# -*- coding: utf-8 -*-

import shutil, os, zipfile, traceback, random
from datetime import datetime
from ordering.util.excel_helper import *
from common import serveFile, Date2Text
from ordering.model import *
from tg import request, config, flash, redirect
import time, zlib
from ordering.util.bin2hex import *
epcobj=upcToepc()


def returnEPC(beginSerail, upc, qty):
    global epcobj
    return epcobj.run(beginSerail, upc, qty)


def upcExportBatch(id_list, qty_list, begin_list, job):
    try:
        fileDir=config.rfid_temp_template
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)
        dlzipFile=os.path.join(fileDir, "%s.zip"%job.no)
        ###########
        #templatePath = os.path.join(os.path.abspath(os.path.curdir),"TEMPLATE/RFID_TEMPLATE.xls")
        templatePath=os.path.join(config.rfid_template, "RFID_TEMPLATE.xls")
        rm=random.randint(1, 1000)
        copyTemplatePath=os.path.join(fileDir, "RFID_TEMPLATE_%d.xls"%rm)
        #copy the template to the dest folder to invoid the confict.
        shutil.copyfile(templatePath, copyTemplatePath)
        fileList=[]
        for index, id in enumerate(id_list):
            row=DBSession.query(Item).get(id)
            #update the last quantity of item.
            row.last_epc=int(begin_list[index])-1+int(qty_list[index])
            result=[]
            serial_no=int(begin_list[index])
            epc_list=returnEPC(int(begin_list[index]), row.upc, int(qty_list[index]))
            for epc in epc_list:
                result.append((row.category.name, \
                               row.part, \
                               row.style_no, \
                               row.size, \
                               row.format, \
                               row.garment_description, \
                               row.style_size, \
                               row.epc_style, \
                               row.upc, \
                               row.rn_no, \
                               "", \
                               row.epc_logo, \
                               row.gtin, \
                               row.vendor, \
                               qty_list[index], \
                               serial_no,
                               epc))
                serial_no+=1
            fileList.append(_upc2Excel(row.upc, result, copyTemplatePath, fileDir, row.part, row.style_no))

            for d in job.details :
                if d.item_id==int(id) :
                    d.epc_code_begin=epc_list[0]
                    d.epc_code_end=epc_list[-1]
                    break

        dlzip=zipfile.ZipFile(dlzipFile, "w", zlib.DEFLATED)
        for fl in fileList:
            logging.info(os.path.abspath(fl))
            dlzip.write(os.path.abspath(str(fl)), os.path.basename(str(fl)))
        dlzip.close()
        try:
            for fl in fileList:
                os.remove(fl)
            os.remove(copyTemplatePath)
        except:
            pass
        return dlzip
    except:
        traceback.print_exc()
        return None


# for jcp, 20120202
def genProducionFile(upc, beginNo, qty):
    try:
        fileDir = config.rfid_temp_template
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)
        dlzipFile = os.path.join(fileDir, "UPC-%s_%s.zip" % (upc, datetime.now().strftime("%Y%m%d%H%M%S")))
        templatePath = os.path.join(config.rfid_template, "RFID_TEMPLATE.xls")
        rm = random.randint(1, 1000)
        copyTemplatePath = os.path.join(fileDir, "RFID_TEMPLATE_%d.xls"%rm)
        #copy the template to the dest folder to invoid the confict.
        shutil.copyfile(templatePath, copyTemplatePath)
        fileList = []
        result = []
        for index, epc in enumerate(returnEPC(beginNo, upc, qty)):
            result.append((upc, 1, beginNo+index, epc))

        fileList.append(_upc2Excel(upc, result, copyTemplatePath, fileDir))
        dlzip = zipfile.ZipFile(dlzipFile, "w", zlib.DEFLATED)
        for fl in fileList:
            dlzip.write(os.path.abspath(str(fl)), os.path.basename(str(fl)))
        dlzip.close()
        try:
            for fl in fileList:
                os.remove(fl)
            os.remove(copyTemplatePath)
        except:
            pass
        return dlzipFile
    except:
        traceback.print_exc()
        return None


def _upc2Excel(upc, data, copyTemplatePath, fileDir):
    xlsFileName = "%s_%s.xls" % (upc, datetime.now().strftime("%Y%m%d%H%M%S"))
    filename = os.path.join(fileDir, xlsFileName)
    #print 'filename',filename

#    print 'input data', time.ctime()
    rfid = RFIDExcel(templatePath=copyTemplatePath, destinationPath=filename)
    try:
        rfid.inputData(data = data)
        rfid.outputData()
        return filename
        #serveFile(filename, "application/x-download", "attachment")
#        print 'input data', time.ctime()
    except:
        traceback.print_exc()
        if rfid:
            rfid.clearData()
        redirect("index")

def reportExport(jdid_list):
    try:
        fileDir=config.report_download_path
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)
        for i in os.listdir(fileDir):
            oldfile=os.path.join(fileDir, i)
            if(time.time()-os.path.getmtime(oldfile)>60*60):
                try:
                    os.remove(oldfile)
                except:
                    pass
        dateStr=datetime.now().strftime("%Y%m%d%H%M%S")
        dlzipFile=os.path.join(fileDir, "report_%s.zip"%dateStr)
        #print dlzipFile

        templatePath=os.path.join(config.rfid_template, "REPORT_TEMPLATE.xls")
        rm=random.randint(1, 1000)
        copyTemplatePath=os.path.join(fileDir, "REPORT_TEMPLATE_%d.xls"%rm)
        #copy the template to the dest folder to invoid the confict.
        shutil.copyfile(templatePath, copyTemplatePath)
        result=[]
        if jdid_list:
            for index, jdid in enumerate(jdid_list):
                jd = DBSession.query(JobDetail).get(jdid)
                serial_begin = jd.serial_begin if jd.serial_begin else 0
                serial_end = jd.serial_end if jd.serial_end else 0
                if serial_begin==0 and serial_end==0:
                    qty = 0
                else:
                    qty = serial_end - serial_begin + 1 
                result.append((
                               jd.header.no, 
                               jd.location.name if jd.location else '',
                               gtinToUpc(jd.gtin),
                               jd.gtin,
                               qty,
                               serial_begin, 
                               serial_end,
                               jd.epc_code_begin, 
                               jd.epc_code_end))
        report_xls=_report2Excel(result, copyTemplatePath, os.path.join(fileDir, "report_%s.xls"%dateStr))
        dlzip=zipfile.ZipFile(dlzipFile, "w", zlib.DEFLATED)
        dlzip.write(os.path.abspath(str(report_xls)), os.path.basename(str(report_xls)))
        dlzip.close()
        try:
            os.remove(copyTemplatePath)
            os.remove(os.path.join(fileDir, "report_%s.xls"%dateStr))
        except:
            pass
        return dlzip, dlzipFile
    except:
        traceback.print_exc()
        return None


def _report2Excel(data, copyTemplatePath, filename):
    rfid=HANESExcel(templatePath = copyTemplatePath, destinationPath = filename)
    try:
        rfid.inputData(data = data)
        rfid.outputData()
        return filename
    except:
        traceback.print_exc()
        if rfid:
            rfid.clearData()
        redirect("index")
