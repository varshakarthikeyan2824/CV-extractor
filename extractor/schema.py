from pydantic import BaseModel


class Experience(BaseModel):
    job_title: str
    company: str
    start_year: int | None = None
    end_year: int | None = None


class Education(BaseModel):
    degree: str
    graduation_year: int | None = None


class CVData(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    summary: str | None = None
    skills: list[str] = []
    experience: list[Experience] = []
    education: list[Education] = []


class InvoiceData(BaseModel):
    invoice_number: str | None = None
    invoice_date: str | None = None
    vendor_name: str | None = None
    customer_name: str | None = None
    subtotal: float | None = None
    tax: float | None = None
    total: float | None = None
