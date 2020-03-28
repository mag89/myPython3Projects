import win32com.client as com_client

outlook = com_client.Dispatch("Outlook.Application")
message = outlook.CreateItem(0)
message.To = "tyr-89@mail.ru"
message.Subject = "TEST"
message.Body = "Simle text || " * 40
message.Send()
outlook, message = None, None
