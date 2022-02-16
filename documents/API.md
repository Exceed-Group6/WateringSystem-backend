(Link ที่ใส่ไว้ยังดึงไม่ได้นะ แค่ใส่ไว้ก่อน)

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

- ดึงข้อมูลต้นไม้ย้อนหลัง ให้ส่ง HTTPRequest แบบ GET ที่
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
