# https://www.youtube.com/watch?v=-SpHPW3RTx8&t=1133s
import boto3
import json
from trp import Document
import PyPDF2



# S3 Bucket Data
# s3BucketName = "demotextractcqpocs"
# PlaindocumentName = "Test2.JPG"
# FormdocumentName = "Test3.JPG"
# TabledocumentName = "Test4.JPG"

file =open("input.pdf",'rb').read()
# print(type(file))
binaryFile = file

# Amazon Textract client
# textractmodule = boto3.client('textract')
textractmodule = boto3.client("textract", aws_access_key_id="AKI*****",
                              aws_secret_access_key="sbxh***********", region_name="us-east-1")


def textract_function():
    #3. TABLE data detection from documents:
    response = textractmodule.analyze_document(
        Document={
            'Bytes': binaryFile
            },
        FeatureTypes=["TABLES"])


    #1 Raw text
    raw_text=''
    for item in response['Blocks']:
        if item['BlockType']=='LINE':
            raw_text+=item['Text']

    print(raw_text)
    doc = Document(response)
    print ('------------- Print Table detected text ------------------------------')
    for page in doc.pages:
        n=0
        for table in page.tables:
            i=1+n
            for r, row in enumerate(table.rows):
                j=1
                itemName  = ""
                for c, cell in enumerate(row.cells):
                    print("Table[{}][{}] = {}".format(r, c, cell.text))
                    
            #         sh1.cell(i,j,cell.text)
            #         j+=1
            #     i+=1
            # n=10


    # json_object = json.dumps(response, indent = 4)
    
    # # Writing to sample.json
    # with open("table.json", "w") as outfile:
    #     outfile.write(json_object)

pdfReader = PyPDF2.PdfReader('current.pdf')
totalpages = len(pdfReader.pages)
print('totalpages ',totalpages)
for i in range(totalpages):
    print('On Page ',i+1)
    output = PyPDF2.PdfWriter()
    output.add_page(pdfReader.pages[i])
    with open("current_page.pdf", "wb") as outputStream:
        output.write(outputStream)
    