"""
Bulk Data Entry - High-volume data input automation.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
import asyncio


@dataclass
class EntryRecord:
    """A single record to enter."""
    data: dict[str, Any]
    identifier: Optional[str] = None


@dataclass
class EntryResult:
    """Result of entering a single record."""
    record: EntryRecord
    success: bool
    error_message: Optional[str] = None


@dataclass
class BulkEntryResult:
    """Result of bulk entry operation."""
    total_records: int
    successful: int
    failed: int
    results: list[EntryResult]
    errors: list[str] = field(default_factory=list)


class BulkDataEntry:
    """
    Automate bulk data entry using Lux.

    Example:
        entry = BulkDataEntry()

        records = [
            EntryRecord({"name": "John", "email": "john@example.com"}),
            EntryRecord({"name": "Jane", "email": "jane@example.com"}),
        ]

        result = await entry.enter_records(
            url="https://crm.example.com/contacts/new",
            records=records
        )
    """

    def __init__(
        self,
        max_steps_per_record: int = 20,
        model: str = "lux-actor-1",
        verbose: bool = False,
        delay_between_records: float = 1.0
    ):
        self.max_steps_per_record = max_steps_per_record
        self.model = model
        self.verbose = verbose
        self.delay_between_records = delay_between_records

    async def enter_records(
        self,
        url: str,
        records: list[EntryRecord],
        submit_button_text: str = "Save",
        new_record_button_text: Optional[str] = "Add New"
    ) -> BulkEntryResult:
        """
        Enter multiple records into a form-based system.

        Args:
            url: URL of the data entry form
            records: List of EntryRecord to enter
            submit_button_text: Text of the submit button
            new_record_button_text: Text of button to start new record

        Returns:
            BulkEntryResult with details of all entries
        """
        results = []
        errors = []

        try:
            from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

            for i, record in enumerate(records):
                agent = AsyncDefaultAgent(
                    max_steps=self.max_steps_per_record,
                    model=self.model
                )

                # Build entry instruction
                instruction = self._build_entry_instruction(
                    url=url,
                    record=record,
                    record_num=i + 1,
                    total_records=len(records),
                    submit_button=submit_button_text,
                    new_record_button=new_record_button_text,
                    is_first=(i == 0)
                )

                try:
                    completed = await agent.execute(
                        instruction,
                        action_handler=AsyncPyautoguiActionHandler(),
                        image_provider=AsyncScreenshotMaker(),
                    )

                    results.append(EntryResult(
                        record=record,
                        success=completed,
                        error_message=None if completed else "Entry did not complete"
                    ))

                except Exception as e:
                    results.append(EntryResult(
                        record=record,
                        success=False,
                        error_message=str(e)
                    ))

                # Delay between records
                if i < len(records) - 1:
                    await asyncio.sleep(self.delay_between_records)

        except ImportError:
            errors.append("oagi package not installed. Run: pip install oagi")

        successful = sum(1 for r in results if r.success)

        return BulkEntryResult(
            total_records=len(records),
            successful=successful,
            failed=len(records) - successful,
            results=results,
            errors=errors
        )

    def _build_entry_instruction(
        self,
        url: str,
        record: EntryRecord,
        record_num: int,
        total_records: int,
        submit_button: str,
        new_record_button: Optional[str],
        is_first: bool
    ) -> str:
        """Build instruction for entering a single record."""
        parts = [f"Data Entry - Record {record_num} of {total_records}"]
        parts.append("")

        if is_first:
            parts.append(f"1. Navigate to {url}")
            step_num = 2
        else:
            if new_record_button:
                parts.append(f"1. Click '{new_record_button}' to start a new entry")
            step_num = 2

        parts.append(f"{step_num}. Fill the form with the following data:")
        for field_name, value in record.data.items():
            parts.append(f"   - {field_name}: {value}")

        parts.append(f"{step_num + 1}. Click '{submit_button}' to save the record")
        parts.append(f"{step_num + 2}. Wait for confirmation that the record was saved")

        return "\n".join(parts)

    async def enter_from_csv(
        self,
        url: str,
        csv_path: str,
        field_mapping: dict[str, str],
        submit_button_text: str = "Save"
    ) -> BulkEntryResult:
        """
        Enter records from a CSV file.

        Args:
            url: URL of the data entry form
            csv_path: Path to the CSV file
            field_mapping: Map of CSV columns to form fields
            submit_button_text: Text of the submit button

        Returns:
            BulkEntryResult with details
        """
        import csv

        records = []

        try:
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Map CSV columns to form fields
                    data = {
                        form_field: row[csv_col]
                        for csv_col, form_field in field_mapping.items()
                        if csv_col in row
                    }
                    records.append(EntryRecord(data=data))

        except Exception as e:
            return BulkEntryResult(
                total_records=0,
                successful=0,
                failed=0,
                results=[],
                errors=[f"Failed to read CSV: {str(e)}"]
            )

        return await self.enter_records(
            url=url,
            records=records,
            submit_button_text=submit_button_text
        )

    async def update_records(
        self,
        search_url: str,
        records: list[EntryRecord],
        search_field: str,
        update_fields: list[str]
    ) -> BulkEntryResult:
        """
        Update existing records by searching and modifying.

        Args:
            search_url: URL of the search/list page
            records: Records with identifier to search and data to update
            search_field: Name of the field to search by
            update_fields: Fields to update

        Returns:
            BulkEntryResult with update details
        """
        results = []

        try:
            from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

            for record in records:
                agent = AsyncDefaultAgent(
                    max_steps=self.max_steps_per_record + 10,
                    model="lux-thinker-1"  # Use Thinker for search+edit
                )

                search_value = record.identifier or record.data.get(search_field, "")

                instruction = f"""
                Update existing record:

                1. Navigate to {search_url}
                2. Search for record with {search_field} = "{search_value}"
                3. Click on the record to edit it
                4. Update the following fields:
                   {self._format_update_fields(record.data, update_fields)}
                5. Save the changes
                """

                try:
                    completed = await agent.execute(
                        instruction,
                        action_handler=AsyncPyautoguiActionHandler(),
                        image_provider=AsyncScreenshotMaker(),
                    )

                    results.append(EntryResult(
                        record=record,
                        success=completed
                    ))

                except Exception as e:
                    results.append(EntryResult(
                        record=record,
                        success=False,
                        error_message=str(e)
                    ))

                await asyncio.sleep(self.delay_between_records)

        except ImportError:
            pass

        successful = sum(1 for r in results if r.success)

        return BulkEntryResult(
            total_records=len(records),
            successful=successful,
            failed=len(records) - successful,
            results=results
        )

    def _format_update_fields(
        self,
        data: dict[str, Any],
        update_fields: list[str]
    ) -> str:
        """Format update fields for instruction."""
        lines = []
        for field in update_fields:
            if field in data:
                lines.append(f"   - {field}: {data[field]}")
        return "\n".join(lines)
