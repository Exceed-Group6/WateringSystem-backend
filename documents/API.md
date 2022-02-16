อ่านแบบ Source นะจะได้อ่านเห็นเว้นวรรคง่ายๆ
(Link ที่ใส่ไว้ยังดึงไม่ได้นะ แค่ใส่ไว้ก่อน)

ในทุกตัวอย่าง 
id จะเป็น int
name, desc จะเป็น str
humidity, light, temp จะเก็บเป็น float ถ้าส่วนไหมเก็ยหลายค่าก็เป็น list ของ float ดูขนาดของ list ได้ที่ตัวนั้นๆ

สำหรับ Front-End

- ดึงข้อมูลสำหรับหน้าหลักที่แสดง Status ชองต้นไม้ทุกต้น ให้ส่ง HTTPRequest แบบ GET ที่
https://ecourse.cpe.ku.ac.th/exceed06/api/getall
จะได้ข้อมูลรูปแบบนี้ มี res amount บอกว่ามีกี่ค่า และ result เป็น list ข้อมูลต้นไม้แต่ละต้น

{
    "res_amount": int,
    "result": [
        {
            "tree_id": 1,
            "base_light": {
                "set": [
                    20,
                    30,
                    40
                ],
                "curret": 26
            },
            "base_humidity": {
                "set": [
                    20,
                    30,
                    40
                ],
                "current": 30
            },
            "base_temp": {
                "set": [
                    20,
                    30,
                    40
                ],
                "current": 38
            }
        },
        {
            "tree_id": 2,
            "base_light": {
                "set": [
                    0,
                    0,
                    0
                ],
                "curret": 0
            },
            "base_humidity": {
                "set": [
                    0,
                    0,
                    0
                ],
                "current": 0
            },
            "base_temp": {
                "set": [
                    0,
                    0,
                    0
                ],
                "current": 0
            }
        }
    ]
}

- ดึงข้อมูลต้นไม้เฉพาะต้น ให้ส่ง HTTPRequest แบบ GET ที่
https://ecourse.cpe.ku.ac.th/exceed06/api/getbyid/{tree_id}
โดยเปลี่ยน {tree_id} เป็นไอดีต้นที่ไม่ที่เท่าไหร่ ถ้าอยากเปลี่ยนเป็นส่ง body มาแทนใส่ในลิงค์เลยทักมานะ
จะได้ข้อมูลกลับมาแบบนี้

{
        "tree_name" : "Temp name",
        "tree_desc" : "lorem possum",
        "cur_bot_status": 1,
        "cur_bot_duration" : 60,
        "base_light" : {
                "set" : [20,30,40],
                "curret" : 26
                },
        "base_humidity" : {
            "set" : [20,30,40],
            "current" : 30
            },
        "base_temp" : {
            "set" : [20,30,40],
            "current" : 38
            },
    }

- ดึงข้อมูลต้นไม้ย้อนหลังเพื่อเอาไปพล็อตกราฟ ให้ส่ง HTTPRequest แบบ GET ที่
https://ecourse.cpe.ku.ac.th/exceed06/api/getrecord/{tree_id}
โดยเปลี่ยน {tree_id} เป็นไอดีต้นที่ไม่ที่เท่าไหร่ ถ้าอยากเปลี่ยนเป็นส่ง body มาแทนใส่ในลิงค์เลยทักมานะ
จะได้ข้อมูลคืนมาแบบนี้
{
        "tree_id" : 1,
        "light" : [] list ข้อมูลย้อนหลัง 42 ตัว,
        "humidity" : [] list ข้อมูลย้อนหลัง 42 ตัว,
        "temp" : [] list ข้อมูลย้อนหลัง 42 ตัว,
}

- ลบต้นไม้ออก ให้ส่ง HTTPRequest แบบ DELETE ที่
https://ecourse.cpe.ku.ac.th/exceed06/api/deletetree/{tree_id}
ถ้าสำเร็จ จะขึ้น 200 และ return
{
        "result" : "success"
}

- ปรับโหมดและระยะเวฃาของ robot ใหม่ update robot status ให้ส่ง HTTPRequest แบบ PUT ที่
https://ecourse.cpe.ku.ac.th/exceed06/api/updatecommand
ส่งมาเเบบ jason file 
{
    "tree_id" : 1,
    "mode_status" : 1, # 0 = on/off mode , 1 = เปิด robot mode
    "duration" : 60
}
ตรงนี้ยังไม่แน่ใจว่าระยะเวลาส่งมาเป็นยังไงนะ ถ้าให้แก้ก็บอกได้ด

- เพิ่มต้นไม้ต้นใหม่ ให้ส่ง HTTPRequest แบบ POST ที่
https://ecourse.cpe.ku.ac.th/exceed06/api/postnewtree
ส่งมาเเบบ JSON file รูปแบบนี้
{
    "tree_id" : 2
    "name" : "new tree"
    "desc" : "describtion of a tree"
    "base_light" : [10,20,30] ＃List ของ int 3 ตัว
    "base_humidity" : [10,20,30]  ＃List ของ int 3 ตัว
    "base_temp" : [10,20,30] ＃List ของ int 3 ตัว
}

สำหรับ Hardware
- อ่านคำสั่งว่าตอนนี้หุ่นยนต์อยู่โหมดไหน ให้ส่ง HTTPRequest แบบ GET ที่
https://ecourse.cpe.ku.ac.th/exceed06/api/getrecord/{tree_id}
เรามีต้นไม้้ต้นเดีนว จะดึงที่ต้นที่ 1 ตลอกเลยก็ใส่ {tree_id} เป็น 1 เลยก็น่าจะได้นะ
จะได้คืนมาแบบนี้ 1 เป็นเปืดบอตรดน้ำ , 0 เป็นกดรดเอง
{
        "tree_id" : 1,
        "mode_status" : 0,
        "duration" : 60
}

- อัพค่าความชื้น แสง อุณหภูมิใหม่ของต้นไม้ ให้ส่ง HTTPRequest แบบ PUT ที่
https://ecourse.cpe.ku.ac.th/exceed06/api/updatetree
โดยให้ส่งไฟล์ JSON รูปแบบนี้มา
｛
    tree_id : 1,
    light : 1200,
    humidity : 38.5,
    temp : 36.5
 ｝
 
- อ่านค่าการกดรดน้ำแบบ manual 
ยังไม่เสร็จ
