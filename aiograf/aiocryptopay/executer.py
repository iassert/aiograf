import asyncio

from aiocryptopay import AioCryptoPay, Networks

from asyncio import Event


class Crypto:
    @staticmethod
    async def paid(invoice_id: int) -> bool:
        Executor.event.set()
        event = Event()

        Executor.invoices[invoice_id] = event

        return await event.wait()


class Executor:
    crypto: AioCryptoPay = None
    defult_delay: float = 0.300

    event = Event()
    invoices: dict[int, Event] = {}


    def __init__(self, token: str, network: Networks = Networks.MAIN_NET):
        Executor.crypto = AioCryptoPay(
            token = token, 
            network = network
        )


    def start_polling(self) -> None:
        asyncio.create_task(Executor.polling())


    @staticmethod
    async def polling() -> None:
        while True:
            if not Executor.invoices:
                await Executor.event.wait()
                Executor.event = Event()

            invoices = await Executor.crypto.get_invoices(
                invoice_ids = [
                    *Executor.invoices.keys()
                ]
            )

            for invoice in invoices:
                if invoice.status == "paid" and invoice.invoice_id in Executor.invoices:
                    Executor.invoices[invoice.invoice_id].set()
                    Executor.invoices.pop(invoice.invoice_id)

            await asyncio.sleep(Executor.defult_delay)
