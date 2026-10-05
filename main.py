import asyncio
import flet as ft
from datetime import datetime, date, time,timedelta
from plyer import notification

from db_config import create_table
from operations import (
    add_task,
    get_tasks_list,
    search_task_name,
    remove_a_task,
    delete_all_tasks,
    update_status,
    update_priority,
    update_notify,
    update_notified_sent,
)


# ============================================================
# COLORS
# ============================================================

NAVY = "#070D24"
CARD = "#101A38"
CARD_2 = "#0C1530"

CYAN = "#19D9FF"
PURPLE = "#7440E8"

WHITE = "#EBF4FF"
MUTED = "#8CA0BD"

GREEN = "#42D77D"
ORANGE = "#FF9633"
RED = "#F24D78"
YELLOW = "#FFD447"


# ============================================================
# STATUS
# ============================================================

PENDING = 0
IN_PROGRESS = 1
COMPLETED = 2
MISSED = 3


def status_text(status):
    if status == COMPLETED:
        return "COMPLETED"
    elif status == MISSED:
        return "MISSED"
    elif status == IN_PROGRESS:
        return "ONGOING"
    return "NOT STARTED"


def status_color(status):
    if status == COMPLETED:
        return GREEN
    elif status == MISSED:
        return RED
    elif status == IN_PROGRESS:
        return CYAN
    return ORANGE


def priority_text(priority):
    if priority == 2:
        return "HIGH"
    elif priority == 1:
        return "MEDIUM"
    return "LOW"


def priority_color(priority):
    if priority == 2:
        return RED
    elif priority == 1:
        return YELLOW
    return GREEN


# ============================================================
# MAIN
# ============================================================

def main(page: ft.Page):

    # --------------------------------------------------------
    # PAGE SETTINGS
    # --------------------------------------------------------

    page.title = "TaskFlow"
    page.bgcolor = NAVY
    page.padding = 0
    page.scroll = ft.ScrollMode.HIDDEN

    # --------------------------------------------------------
    # FIXED APP WINDOW SIZE
    # --------------------------------------------------------

    page.window.width = 400
    page.window.height = 800

    page.window.min_width = 400
    page.window.max_width = 400

    page.window.min_height = 800
    page.window.max_height = 800

    page.window.resizable = False
    page.window.maximizable = False

    # --------------------------------------------------------
    # DATABASE
    # --------------------------------------------------------

    create_table()

    # --------------------------------------------------------
    # MAIN CONTENT
    # --------------------------------------------------------

    content = ft.Container(
        expand=True,
        padding=ft.Padding(
            left=18,
            right=18,
            top=20,
            bottom=10,
        ),
    )

    current_page = 0

    # ========================================================
    # HELPERS
    # ========================================================

    def show_snack(message):

        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(
                    message,
                    color=WHITE,
                ),
                bgcolor = CARD
            )
        )

    def close_dialog(dialog):

        dialog.open = False
        page.update()

    # ========================================================
    # NAVIGATION
    # ========================================================

    nav_buttons = [
        ft.NavigationBarDestination(
            icon=ft.Icons.HOME_OUTLINED,
            selected_icon=ft.Icons.HOME,
            label="HOME",
        ),
        ft.NavigationBarDestination(
            icon=ft.Icons.ADD_CIRCLE_OUTLINE,
            selected_icon=ft.Icons.ADD_CIRCLE,
            label="ADD",
        ),
        ft.NavigationBarDestination(
            icon=ft.Icons.BAR_CHART_OUTLINED,
            selected_icon=ft.Icons.BAR_CHART,
            label="STATS",
        ),
        ft.NavigationBarDestination(
            icon=ft.Icons.SETTINGS_OUTLINED,
            selected_icon=ft.Icons.SETTINGS,
            label="SETTINGS",
        ),
    ]

    navigation = ft.NavigationBar(
        destinations=nav_buttons,
        selected_index=0,
        bgcolor=CARD_2,
        indicator_color=PURPLE,
        on_change=lambda e: change_page(
            e.control.selected_index
        ),
    )

    def change_page(index):

        nonlocal current_page

        current_page = index

        navigation.selected_index = index

        if index == 0:
            show_home()

        elif index == 1:
            show_add_task()

        elif index == 2:
            show_statistics()

        elif index == 3:
            show_settings()

        page.update()

    # ========================================================
    # STAT CARD
    # ========================================================

    def stat_card(title, value, icon, color):

        return ft.Container(
            expand=True,
            padding=15,
            bgcolor=CARD,
            border_radius=15,
            border=ft.Border.all(
                1,
                "#18264B",
            ),
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                icon,
                                color=color,
                                size=22,
                            ),
                            ft.Text(
                                title,
                                size=11,
                                color=MUTED,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ]
                    ),
                    ft.Text(
                        str(value),
                        size=26,
                        color=WHITE,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
            ),
        )

    # ========================================================
    # TASK CARD
    # ========================================================

    def task_card(task):

        task_no = task[0]
        task_name = task[1]
        start = task[2]
        deadline = task[3]
        status = task[4]
        notify = task[5]
        priority = task[6]
        description = task[7] or ""

        # ----------------------------------------------------
        # MARK AS COMPLETED
        # ----------------------------------------------------

        def mark_completed(e):

            if status != COMPLETED:

                if update_status(
                    task_no,
                    COMPLETED
                ):
                    show_snack(
                        "Task marked as completed."
                    )

                    refresh_home()

        # ----------------------------------------------------
        # CHANGE PRIORITY
        # ----------------------------------------------------

        def change_priority(e):

            new_priority = (
                2
                if e.control.value
                else 0
            )

            if update_priority(
                task_no,
                new_priority
            ):
                refresh_home()

        # ----------------------------------------------------
        # CHANGE NOTIFICATION
        # ----------------------------------------------------

        def change_notification(e):

            new_notify = (
                1
                if e.control.value
                else 0
            )

            if update_notify(
                task_no,
                new_notify
            ):
                refresh_home()

        # ----------------------------------------------------
        # DELETE TASK
        # ----------------------------------------------------

        def delete_task(e):

            def confirm_delete(_):

                if remove_a_task(task_no):

                    close_dialog(dialog)

                    refresh_home()

                    show_snack(
                        "Task deleted successfully."
                    )

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(
                    "Delete Task",
                    color=WHITE,
                ),
                content=ft.Text(
                    f'Do you want to delete "{task_name}"?',
                    color=MUTED,
                ),
                actions=[
                    ft.TextButton(
                        "CANCEL",
                        on_click=lambda _: close_dialog(
                            dialog
                        ),
                    ),
                    ft.TextButton(
                        "DELETE",
                        on_click=confirm_delete,
                    ),
                ],
            )

            page.show_dialog(dialog)

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        status_label = ft.Text(
            status_text(status),
            color=status_color(status),
            size=14,
            weight=ft.FontWeight.BOLD,
        )

        # ----------------------------------------------------
        # PRIORITY SWITCH
        # ----------------------------------------------------

        priority_switch = ft.Switch(
            value=priority == 2,
            active_color=RED,
            label="Priority",
            on_change=change_priority,
        )

        # ----------------------------------------------------
        # NOTIFICATION SWITCH
        # ----------------------------------------------------

        notification_switch = ft.Switch(
            value=notify == 1,
            active_color=CYAN,
            label="Notification",
            on_change=change_notification,
        )

        # ----------------------------------------------------
        # MARK COMPLETED BUTTON
        # ----------------------------------------------------

        mark_completed_button = ft.Container(
            padding=ft.Padding(
                left=12,
                right=12,
                top=8,
                bottom=8,
            ),
            border_radius=10,
            bgcolor=(
                GREEN + "22"
                if status == COMPLETED
                else PURPLE + "22"
            ),
            border=ft.Border.all(
                1,
                GREEN
                if status == COMPLETED
                else PURPLE,
            ),
            content=ft.Row(
                spacing=6,
                tight=True,
                controls=[
                    ft.Icon(
                        (
                            ft.Icons.CHECK_CIRCLE
                            if status == COMPLETED
                            else ft.Icons.CHECK_CIRCLE_OUTLINE
                        ),
                        size=17,
                        color=(
                            GREEN
                            if status == COMPLETED
                            else PURPLE
                        ),
                    ),
                    ft.Text(
                        (
                            "COMPLETED"
                            if status == COMPLETED
                            else "MARK AS COMPLETED"
                        ),
                        size=10,
                        color=(
                            GREEN
                            if status == COMPLETED
                            else WHITE
                        ),
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
            ),
            on_click=mark_completed,
        )

        # ----------------------------------------------------
        # TASK DETAILS
        # ----------------------------------------------------

        details = ft.Column(
            spacing=8,
            controls=[

                # TASK NAME
                ft.Text(
                    task_name,
                    size=17,
                    color=(
                        MUTED
                        if status == COMPLETED
                        else WHITE
                    ),
                    weight=ft.FontWeight.BOLD,
                    style=(
                        ft.TextStyle(
                            decoration=(
                                ft.TextDecoration.LINE_THROUGH
                            )
                        )
                        if status == COMPLETED
                        else None
                    ),
                ),

                # DESCRIPTION
                ft.Text(
                    description,
                    size=12,
                    color=MUTED,
                    visible=bool(description),
                ),

                # STATUS
                ft.Row(
                    spacing=8,
                    vertical_alignment=(
                        ft.CrossAxisAlignment.CENTER
                    ),
                    controls=[
                        ft.Text(
                            "Status",
                            size=11,
                            color=MUTED,
                        ),
                        status_label,
                    ],
                ),

                # PRIORITY + NOTIFICATION
                ft.Row(
                    wrap=True,
                    spacing=5,
                    controls=[
                        priority_switch,
                        notification_switch,
                    ],
                ),

                # START
                ft.Row(
                    spacing=6,
                    controls=[
                        ft.Icon(
                            ft.Icons.ACCESS_TIME,
                            size=14,
                            color=MUTED,
                        ),
                        ft.Text(
                            f"Start: {start}",
                            size=11,
                            color=MUTED,
                        ),
                    ],
                ),

                # DEADLINE
                ft.Row(
                    spacing=6,
                    controls=[
                        ft.Icon(
                            ft.Icons.CALENDAR_TODAY,
                            size=14,
                            color=MUTED,
                        ),
                        ft.Text(
                            f"Deadline: {deadline}",
                            size=11,
                            color=MUTED,
                        ),
                    ],
                ),

                # MARK AS COMPLETED
                mark_completed_button,
            ],
        )

        return ft.Container(
            padding=15,
            margin=ft.Margin(
                left=0,
                right=0,
                top=5,
                bottom=5,
            ),
            bgcolor=CARD,
            border_radius=16,
            border=ft.Border.all(
                1,
                "#18264B",
            ),
            content=ft.Row(
                vertical_alignment=(
                    ft.CrossAxisAlignment.START
                ),
                controls=[

                    ft.Container(
                        expand=True,
                        content=details,
                    ),

                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=RED,
                        tooltip="Delete",
                        on_click=delete_task,
                    ),
                ],
            ),
        )

    # ========================================================
    # HOME
    # ========================================================

       # ========================================================
    # HOME + CALENDAR
    # ========================================================

    search_field = ft.TextField(
        hint_text="Search tasks...",
        prefix_icon=ft.Icons.SEARCH,
        bgcolor=CARD,
        border_color="#1C2A50",
        focused_border_color=CYAN,
        color=WHITE,
        hint_style=ft.TextStyle(
            color=MUTED,
        ),
        border_radius=12,
        on_change=lambda e: refresh_home(),
    )

    total_text = ft.Text(
        "0",
        size=26,
        color=WHITE,
        weight=ft.FontWeight.BOLD,
    )

    completed_text = ft.Text(
        "0",
        size=26,
        color=WHITE,
        weight=ft.FontWeight.BOLD,
    )

    pending_text = ft.Text(
        "0",
        size=26,
        color=WHITE,
        weight=ft.FontWeight.BOLD,
    )

    progress_value = ft.Text(
        "0%",
        size=26,
        color=CYAN,
        weight=ft.FontWeight.BOLD,
    )

    progress_bar = ft.ProgressBar(
        value=0,
        color=CYAN,
        bgcolor="#1B2848",
        height=8,
    )

    # --------------------------------------------------------
    # CALENDAR VARIABLES
    # --------------------------------------------------------

    selected_calendar_date = date.today()

    calendar_month = date.today().replace(
        day=1
    )

    calendar_grid = ft.Column(
        spacing=3,
    )

    calendar_month_text = ft.Text(
        "",
        size=15,
        color=WHITE,
        weight=ft.FontWeight.BOLD,
    )

    selected_date_text = ft.Text(
        "",
        size=14,
        color=CYAN,
        weight=ft.FontWeight.BOLD,
    )

    calendar_task_column = ft.Column(
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    # ========================================================
    # TASK DATE HELPERS
    # ========================================================

    def update_task_statuses():
        now = datetime.now()

        tasks = get_tasks_list()

        for task in tasks:
            task_id = task[0]
            task_name = task[1]
            priority = task[6]
            notified_sent = task[8] if len(task) > 8 else 0
            
            start_time = datetime.strptime(
                task[2],
                "%Y-%m-%d %H:%M"
            )
            deadline = datetime.strptime(
                task[3],
                "%Y-%m-%d %H:%M"
            )

            # Don't change completed tasks
            if task[4] == COMPLETED:
                continue

            if now < start_time:
                status = PENDING

            elif start_time <= now <= deadline:
                status = IN_PROGRESS
                
                # Check for critical task notification (priority == 2 is HIGH)
                if priority == 2 and notified_sent == 0:
                    time_to_deadline = deadline - now
                    # Notify if within 5 minutes (300 seconds) of deadline
                    if timedelta(seconds=0) <= time_to_deadline <= timedelta(minutes=5):
                        try:
                            notification.notify(
                                title="Critical Task Reminder",
                                message=f"Task '{task_name}' is due in less than 5 minutes!",
                                app_name="TaskFlow",
                                timeout=10
                            )
                            update_notified_sent(task_id, 1)
                        except Exception as e:
                            print(f"Failed to send notification: {e}")

            else:
                status = MISSED

            update_status(
                task_id,
                status
            )

    def task_belongs_to_date(
        task,
        selected_date
    ):
        start_datetime = datetime.strptime(
            task[2],
            "%Y-%m-%d %H:%M"
        )

        deadline_datetime = datetime.strptime(
            task[3],
            "%Y-%m-%d %H:%M"
        )

        start_date = start_datetime.date()
        deadline_date = deadline_datetime.date()

        return (
            start_date
            <= selected_date
            <= deadline_date
        )

    def get_tasks_for_date(
        selected_date
    ):
        tasks = get_tasks_list()

        query = search_field.value.strip().lower()

        result = []

        for task in tasks:

            # Search filter
            if query:
                task_name = str(
                    task[1]
                ).lower()

                description = str(
                    task[7]
                ).lower()

                if (
                    query not in task_name
                    and query not in description
                ):
                    continue

            # Date filter
            if task_belongs_to_date(
                task,
                selected_date
            ):
                result.append(task)

        return result

    def date_has_task(
        calendar_date
    ):
        tasks = get_tasks_list()

        for task in tasks:
            if task_belongs_to_date(
                task,
                calendar_date
            ):
                return True

        return False

    def select_calendar_date(selected_date):
        nonlocal selected_calendar_date

        selected_calendar_date = selected_date

        render_calendar()
        render_selected_date_tasks()

        page.update()

    def render_selected_date_tasks():
        calendar_task_column.controls.clear()

        selected_date_text.value = (
            selected_calendar_date.strftime("%d %B %Y")
        )

        tasks = get_tasks_for_date(
            selected_calendar_date
        )

        if not tasks:
            calendar_task_column.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No tasks for this date",
                        color=MUTED,
                        size=14,
                    ),
                    padding=20,
                    alignment=ft.Alignment.CENTER,
                )
            )
        else:
            for task in tasks:
                calendar_task_column.controls.append(
                    task_card(task)
                )

    def get_calendar_status_colors(calendar_date):
        tasks = get_tasks_list()

        colors = []

        for task in tasks:
            if not task_belongs_to_date(task, calendar_date):
                continue

            status = task[4]

            if status == PENDING:
                color = ORANGE
            elif status == MISSED:
                color = RED
            elif status == COMPLETED:
                color = GREEN
            elif status == IN_PROGRESS:
                color = CYAN
            else:
                continue

            if color not in colors:
                colors.append(color)

        return colors
    
    def calendar_day_cell(calendar_date):
        status_colors = get_calendar_status_colors(calendar_date)
        is_selected = calendar_date == selected_calendar_date
        is_today = calendar_date == date.today()

        controls = [
            ft.Text(
                str(calendar_date.day),
                size=13,
                color=WHITE,
                weight=(
                    ft.FontWeight.BOLD
                    if is_selected or is_today
                    else ft.FontWeight.NORMAL
                ),
            )
        ]

        if status_colors:
            controls.append(
                ft.Row(
                    controls=[
                        ft.Container(
                            width=5,
                            height=5,
                            bgcolor=color,
                            border_radius=10,
                        )
                        for color in status_colors
                    ],
                    spacing=2,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
        else:
            controls.append(
                ft.Container(
                    width=5,
                    height=5,
                )
            )

        return ft.Container(
            width=43,
            height=43,
            bgcolor=(
                PURPLE + "55"
                if is_selected
                else CARD
            ),
            border_radius=10,
            border=(
                ft.Border.all(1, CYAN)
                if is_today
                else None
            ),
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                controls=controls,
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                alignment=(
                    ft.MainAxisAlignment.CENTER
                ),
                spacing=2,
            ),
            on_click=lambda e, d=calendar_date:
                select_calendar_date(d),
        )

    # ========================================================
    # CALENDAR RENDERING
    # ========================================================

    def render_calendar():
        calendar_grid.controls.clear()

        calendar_month_text.value = (
            calendar_month.strftime("%B %Y")
        )

        # Calculate the weekday offset
        # Sunday = 0, Monday = 1, ..., Saturday = 6
        first_day_offset = (
            calendar_month.weekday() + 1
        ) % 7

        # Get the first day of the next month
        if calendar_month.month == 12:
            next_month = date(
                calendar_month.year + 1,
                1,
                1
            )
        else:
            next_month = date(
                calendar_month.year,
                calendar_month.month + 1,
                1
            )

        # Calculate the number of days in the month
        days_in_month = (
            next_month - calendar_month
        ).days

        cells = []

        # Add empty cells before the first day
        for _ in range(first_day_offset):
            cells.append(
                ft.Container(
                    width=43,
                    height=43,
                )
            )

        # Add all days of the current month
        for day_number in range(
            1,
            days_in_month + 1
        ):
            current_date = date(
                calendar_month.year,
                calendar_month.month,
                day_number,
            )

            cells.append(
                calendar_day_cell(
                    current_date
                )
            )

        # Add empty cells after the last day
        while len(cells) % 7 != 0:
            cells.append(
                ft.Container(
                    width=43,
                    height=43,
                )
            )

        # Create calendar rows
        for i in range(
            0,
            len(cells),
            7
        ):
            calendar_grid.controls.append(
                ft.Row(
                    controls=cells[i:i + 7],
                    spacing=3,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

    # ========================================================
    # CALENDAR NAVIGATION
    # ========================================================

    def previous_month(e):
        nonlocal calendar_month

        if calendar_month.month == 1:
            calendar_month = date(
                calendar_month.year - 1,
                12,
                1
            )
        else:
            calendar_month = date(
                calendar_month.year,
                calendar_month.month - 1,
                1
            )

        render_calendar()
        page.update()

    def next_month(e):
        nonlocal calendar_month

        if calendar_month.month == 12:
            calendar_month = date(
                calendar_month.year + 1,
                1,
                1
            )
        else:
            calendar_month = date(
                calendar_month.year,
                calendar_month.month + 1,
                1
            )

        render_calendar()
        page.update()

    def go_to_today(e):
        nonlocal calendar_month
        nonlocal selected_calendar_date

        selected_calendar_date = date.today()

        calendar_month = date.today().replace(
            day=1
        )

        render_calendar()
        render_selected_date_tasks()

        page.update()

    

    # ========================================================
    # CALENDAR DAY CELL
    # ========================================================


    # ========================================================
    # HOME UI
    # ========================================================

    calendar_header = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.CHEVRON_LEFT,
                icon_color=WHITE,
                on_click=previous_month,
            ),

            calendar_month_text,

            ft.IconButton(
                icon=ft.Icons.CHEVRON_RIGHT,
                icon_color=WHITE,
                on_click=next_month,
            ),

            ft.Container(
                expand=True,
            ),

            ft.TextButton(
                "TODAY",
                on_click=go_to_today,
            ),
        ],
        vertical_alignment=(
            ft.CrossAxisAlignment.CENTER
        ),
    )

    calendar_week_header = ft.Row(
        controls=[
            ft.Container(
                width=43,
                content=ft.Text(
                    day,
                    size=11,
                    color=MUTED,
                    text_align=ft.TextAlign.CENTER,
                ),
            )
            for day in [
                "SUN",
                "MON",
                "TUE",
                "WED",
                "THU",
                "FRI",
                "SAT",
            ]
        ],
        spacing=3,
        alignment=(
            ft.MainAxisAlignment.CENTER
        ),
    )

    calendar_card = ft.Container(
        bgcolor=CARD,
        border_radius=16,
        padding=12,
        content=ft.Column(
            controls=[
                calendar_header,

                calendar_week_header,

                ft.Divider(
                    color="#1C2A50",
                    height=1,
                ),

                calendar_grid,
            ],
            spacing=8,
        ),
    )

    # ========================================================
    # REFRESH HOME
    # ========================================================

    def refresh_home(e=None):

        # Update task statuses first
        update_task_statuses()

        tasks = get_tasks_list()

        # Search
        query = search_field.value.strip()

        if query:
            filtered_tasks = search_task_name(
                query
            )
        else:
            filtered_tasks = tasks

        # Statistics
        total = len(filtered_tasks)

        completed = sum(
            1
            for task in filtered_tasks
            if task[4] == COMPLETED
        )

        pending = sum(
            1
            for task in filtered_tasks
            if task[4] in (
                PENDING,
                IN_PROGRESS
            )
        )

        # Progress
        progress = (
            completed / total
            if total > 0
            else 0
        )

        total_text.value = str(total)

        completed_text.value = str(
            completed
        )

        pending_text.value = str(
            pending
        )

        progress_value.value = (
            f"{int(progress * 100)}%"
        )

        progress_bar.value = progress

        # Refresh calendar
        render_calendar()

        # Refresh selected date tasks
        render_selected_date_tasks()

        page.update()

    # ========================================================
    # AUTOMATIC STATUS UPDATE
    # ========================================================

    async def automatic_status_update():

        while True:

            update_task_statuses()

            render_calendar()
            render_selected_date_tasks()

            page.update()

            await asyncio.sleep(60)

    # ========================================================
    # SHOW HOME
    # ========================================================

    home_content=ft.Column(
        spacing=0,
        expand=True,
scroll=ft.ScrollMode.AUTO,
    )
    content.content = home_content
    def show_home():

        home_content.controls.clear()

        home_content.controls.append(
            ft.Column(
                controls=[

                    # Header
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "TASKFLOW",
                                        size=24,
                                        color=CYAN,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        "Your Future Planner",
                                        size=12,
                                        color=MUTED,
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                    ),

                    ft.Container(height=8),

                    # Search
                    search_field,

                    ft.Container(height=8),

                   # Statistics
ft.Column(
    controls=[
        ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.ANALYTICS,
                                        color=CYAN,
                                        size=20,
                                    ),
                                    ft.Text(
                                        "TOTAL",
                                        size=10,
                                        color=MUTED,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                                spacing=8,
                            ),
                            total_text,
                        ],
                        spacing=4,
                    ),
                    bgcolor=CARD,
                    border_radius=12,
                    padding=12,
                    expand=True,
                ),

                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.CHECK_CIRCLE_OUTLINE,
                                        color=GREEN,
                                        size=20,
                                    ),
                                    ft.Text(
                                        "COMPLETED",
                                        size=10,
                                        color=MUTED,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                                spacing=8,
                            ),
                            completed_text,
                        ],
                        spacing=4,
                    ),
                    bgcolor=CARD,
                    border_radius=12,
                    padding=12,
                    expand=True,
                ),
            ],
            spacing=8,
        ),

        ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.PENDING_ACTIONS,
                                        color=ORANGE,
                                        size=20,
                                    ),
                                    ft.Text(
                                        "PENDING",
                                        size=10,
                                        color=MUTED,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                                spacing=8,
                            ),
                            pending_text,
                        ],
                        spacing=4,
                    ),
                    bgcolor=CARD,
                    border_radius=12,
                    padding=12,
                    expand=True,
                ),

                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.TRENDING_UP,
                                        color=PURPLE,
                                        size=20,
                                    ),
                                    ft.Text(
                                        "PROGRESS",
                                        size=10,
                                        color=MUTED,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                                spacing=8,
                            ),
                            progress_value,
                        ],
                        spacing=4,
                    ),
                    bgcolor=CARD,
                    border_radius=12,
                    padding=12,
                    expand=True,
                ),
            ],
            spacing=8,
        ),
    ],
    spacing=8,
),

                    # Calendar Header
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.CHEVRON_LEFT,
                                icon_color=WHITE,
                                on_click=previous_month,
                            ),

                            ft.Container(
                                content=calendar_month_text,
                                alignment=ft.Alignment(0, 0),
                                expand=True,
                            ),

                            ft.TextButton(
                                "TODAY",
                                on_click=go_to_today,
                            ),

                            ft.IconButton(
                                icon=ft.Icons.CHEVRON_RIGHT,
                                icon_color=WHITE,
                                on_click=next_month,
                            ),
                        ],
                    ),

                    # Calendar
                    ft.Container(
                        content=ft.Column(
                            controls=[

                                ft.Row(
                                    controls=[
                                        ft.Text("SUN", size=9, color=MUTED, expand=True, text_align=ft.TextAlign.CENTER),
                                        ft.Text("MON", size=9, color=MUTED, expand=True, text_align=ft.TextAlign.CENTER),
                                        ft.Text("TUE", size=9, color=MUTED, expand=True, text_align=ft.TextAlign.CENTER),
                                        ft.Text("WED", size=9, color=MUTED, expand=True, text_align=ft.TextAlign.CENTER),
                                        ft.Text("THU", size=9, color=MUTED, expand=True, text_align=ft.TextAlign.CENTER),
                                        ft.Text("FRI", size=9, color=MUTED, expand=True, text_align=ft.TextAlign.CENTER),
                                        ft.Text("SAT", size=9, color=MUTED, expand=True, text_align=ft.TextAlign.CENTER),
                                    ],
                                    spacing=3,
                                ),

                                calendar_grid,

                            ],
                            spacing=6,
                        ),
                        bgcolor=CARD,
                        border_radius=14,
                        padding=10,
                    ),

                    ft.Container(height=10),

                    # Selected date
                    selected_date_text,

                    ft.Container(height=4),

                    # Tasks for selected date
                    calendar_task_column,

                ],
                spacing=0,
            )
        )

        content.content = home_content
        refresh_home()
    

    # ========================================================
    # DATE PICKER
    # ========================================================

    def create_date_picker(
        title,
        callback,
        initial_value=None,
    ):

        picker = ft.DatePicker(
            current_date=(
                initial_value
                or date.today()
            ),
            value=initial_value,
            entry_mode=(
                ft.DatePickerEntryMode.CALENDAR_ONLY
            ),
            help_text=title,
            confirm_text="SELECT",
            cancel_text="CANCEL",
            on_change=callback,
        )

        return picker

    # ========================================================
    # TIME PICKER
    # ========================================================

    def create_time_picker(
        title,
        callback,
        initial_value=None,
    ):

        picker = ft.TimePicker(
            value=(
                initial_value
                or time(
                    hour=datetime.now().hour,
                    minute=datetime.now().minute,
                )
            ),
            entry_mode=(
                ft.TimePickerEntryMode.DIAL_ONLY
            ),
            help_text=title,
            confirm_text="SELECT",
            cancel_text="CANCEL",
            on_change=callback,
        )

        return picker

    # ========================================================
    # ADD TASK
    # ========================================================

    def show_add_task():

        task_name = ft.TextField(
            label="Task name",
            hint_text="Enter task name",
            color=WHITE,
            label_style=ft.TextStyle(
                color=MUTED,
            ),
            border_color="#1C2A50",
            focused_border_color=CYAN,
            bgcolor=CARD,
            border_radius=12,
        )

        description = ft.TextField(
            label="Description",
            hint_text="Optional description",
            multiline=True,
            min_lines=3,
            max_lines=5,
            color=WHITE,
            label_style=ft.TextStyle(
                color=MUTED,
            ),
            border_color="#1C2A50",
            focused_border_color=CYAN,
            bgcolor=CARD,
            border_radius=12,
        )

        # ----------------------------------------------------
        # DATE/TIME VALUES
        # ----------------------------------------------------

        start_date = None
        start_time = None

        deadline_date = None
        deadline_time = None

        # ----------------------------------------------------
        # DISPLAY FIELDS
        # ----------------------------------------------------

        start_field = ft.TextField(
            label="Start",
            hint_text="Select date and time",
            read_only=True,
            color=WHITE,
            label_style=ft.TextStyle(
                color=MUTED,
            ),
            border_color="#1C2A50",
            focused_border_color=CYAN,
            bgcolor=CARD,
            border_radius=12,
            expand=True,
        )

        deadline_field = ft.TextField(
            label="Deadline",
            hint_text="Select date and time",
            read_only=True,
            color=WHITE,
            label_style=ft.TextStyle(
                color=MUTED,
            ),
            border_color="#1C2A50",
            focused_border_color=CYAN,
            bgcolor=CARD,
            border_radius=12,
            expand=True,
        )

        # ----------------------------------------------------
        # START DATE
        # ----------------------------------------------------

        def start_date_changed(e):
            nonlocal start_date

            selected = e.control.value

            if selected is not None:
                if isinstance(selected, datetime):
                    start_date = (selected + timedelta(hours=12)).date()
                else:
                    start_date = selected

                update_start_field()

        # ----------------------------------------------------
        # START TIME
        # ----------------------------------------------------

        def start_time_changed(e):

            nonlocal start_time

            start_time = e.control.value

            if start_time is not None:
                update_start_field()

        # ----------------------------------------------------
        # UPDATE START FIELD
        # ----------------------------------------------------

        def update_start_field():

            if start_date and start_time:

                start_field.value = (
                    f"{start_date.strftime('%Y-%m-%d')} "
                    f"{start_time.strftime('%H:%M')}"
                )

            elif start_date:

                start_field.value = (
                    start_date.strftime(
                        "%d-%b-%y"
                    )
                )

            page.update()

        start_date_picker = create_date_picker(
            "Select start date",
            start_date_changed,
        )

        start_time_picker = create_time_picker(
            "Select start time",
            start_time_changed,
        )

        def open_start_date(_):

            page.show_dialog(
                start_date_picker
            )

        def open_start_time(_):

            page.show_dialog(
                start_time_picker
            )

        # ----------------------------------------------------
        # DEADLINE DATE
        # ----------------------------------------------------

        def deadline_date_changed(e):
            nonlocal deadline_date

            selected = e.control.value

            if selected is not None:
                if isinstance(selected, datetime):
                    deadline_date = (selected + timedelta(hours=12)).date()
                else:
                    deadline_date = selected

                update_deadline_field()

        # ----------------------------------------------------
        # DEADLINE TIME
        # ----------------------------------------------------

        def deadline_time_changed(e):

            nonlocal deadline_time

            deadline_time = e.control.value

            if deadline_time is not None:
                update_deadline_field()

        # ----------------------------------------------------
        # UPDATE DEADLINE FIELD
        # ----------------------------------------------------

        def update_deadline_field():

            if deadline_date and deadline_time:

                deadline_field.value = (
                    f"{deadline_date.strftime('%Y-%m-%d')} "
                    f"{deadline_time.strftime('%H:%M')}"
                )

            elif deadline_date:

                deadline_field.value = (
                    deadline_date.strftime(
                        "%d-%b-%y"
                    )
                )

            page.update()

        deadline_date_picker = create_date_picker(
            "Select deadline date",
            deadline_date_changed,
        )

        deadline_time_picker = create_time_picker(
            "Select deadline time",
            deadline_time_changed,
        )

        def open_deadline_date(_):

            page.show_dialog(
                deadline_date_picker
            )

        def open_deadline_time(_):

            page.show_dialog(
                deadline_time_picker
            )

        # ----------------------------------------------------
        # PRIORITY
        # ----------------------------------------------------

        priority_switch = ft.Switch(
            label="High priority",
            value=False,
            active_color=RED,
        )

        # ----------------------------------------------------
        # NOTIFICATION
        # ----------------------------------------------------

        notify_switch = ft.Switch(
            label="Reminder",
            value=False,
            active_color=CYAN,
        )

        # ----------------------------------------------------
        # SAVE TASK
        # ----------------------------------------------------

        def save_task(_):

            if not task_name.value.strip():

                show_snack(
                    "Please enter a task name."
                )

                return

            if not start_date or not start_time:

                show_snack(
                    "Please select start date and time."
                )

                return

            if not deadline_date or not deadline_time:

                show_snack(
                    "Please select deadline date and time."
                )

                return

            start_value = (
                f"{start_date.strftime('%Y-%m-%d')} "
                f"{start_time.strftime('%H:%M')}"
            )

            deadline_value = (
                f"{deadline_date.strftime('%Y-%m-%d')} "
                f"{deadline_time.strftime('%H:%M')}"
            )

            # ------------------------------------------------
            # VALIDATE START / DEADLINE
            # ------------------------------------------------
            # A task cannot have a deadline before or exactly
            # at its start time. This also prevents a future
            # start time from being paired with an already
            # expired deadline, which could otherwise make the
            # task appear as MISSED.
            start_datetime = datetime.strptime(
                start_value,
                "%Y-%m-%d %H:%M"
            )

            deadline_datetime = datetime.strptime(
                deadline_value,
                "%Y-%m-%d %H:%M"
            )

            if deadline_datetime <= start_datetime:
                show_snack(
                    "Deadline must be after the start time."
                )
                return

            success = add_task(
                task_name.value.strip(),
                start_value,
                deadline_value,
                description.value.strip(),
            )

            if not success:

                show_snack(
                    "Failed to add task."
                )

                return

            # Get latest task
            tasks = get_tasks_list()

            if tasks:

                latest_task = max(
                    tasks,
                    key=lambda x: x[0],
                )

                task_no = latest_task[0]

                priority = (
                    2
                    if priority_switch.value
                    else 0
                )

                notify = (
                    1
                    if notify_switch.value
                    else 0
                )

                update_priority(
                    task_no,
                    priority,
                )

                update_notify(
                    task_no,
                    notify,
                )

            show_snack(
                "Task added successfully."
            )

            task_name.value = ""
            description.value = ""

            start_field.value = ""
            deadline_field.value = ""

            priority_switch.value = False
            notify_switch.value = False

            change_page(0)

        # ----------------------------------------------------
        # ADD SCREEN
        # ----------------------------------------------------

        content.content = ft.Column(
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
            controls=[

                ft.Text(
                    "ADD NEW TASK",
                    size=25,
                    color=CYAN,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Text(
                    "Plan your next task",
                    size=13,
                    color=MUTED,
                ),

                task_name,

                # START
                ft.Text(
                    "START DATE & TIME",
                    size=11,
                    color=MUTED,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Row(
                    spacing=8,
                    controls=[
                        start_field,

                        ft.IconButton(
                            icon=ft.Icons.CALENDAR_MONTH,
                            icon_color=CYAN,
                            bgcolor=CARD,
                            tooltip="Select date",
                            on_click=open_start_date,
                        ),

                        ft.IconButton(
                            icon=ft.Icons.ACCESS_TIME,
                            icon_color=PURPLE,
                            bgcolor=CARD,
                            tooltip="Select time",
                            on_click=open_start_time,
                        ),
                    ],
                ),

                # DEADLINE
                ft.Text(
                    "DEADLINE DATE & TIME",
                    size=11,
                    color=MUTED,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Row(
                    spacing=8,
                    controls=[
                        deadline_field,

                        ft.IconButton(
                            icon=ft.Icons.CALENDAR_MONTH,
                            icon_color=CYAN,
                            bgcolor=CARD,
                            tooltip="Select date",
                            on_click=open_deadline_date,
                        ),

                        ft.IconButton(
                            icon=ft.Icons.ACCESS_TIME,
                            icon_color=PURPLE,
                            bgcolor=CARD,
                            tooltip="Select time",
                            on_click=open_deadline_time,
                        ),
                    ],
                ),

                description,

                ft.Container(
                    padding=15,
                    bgcolor=CARD,
                    border_radius=14,
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            priority_switch,
                            notify_switch,
                        ],
                    ),
                ),

                ft.Container(
                    height=55,
                    border_radius=14,
                    bgcolor=PURPLE,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "SAVE TASK",
                        color=WHITE,
                        size=15,
                        weight=ft.FontWeight.BOLD,
                    ),
                    on_click=save_task,
                ),
            ],
        )

        page.update()

    # ========================================================
    # STATISTICS
    # ========================================================

    def show_statistics():

        tasks = get_tasks_list()

        total = len(tasks)

        completed = sum(
            1
            for task in tasks
            if task[4] == COMPLETED
        )

        pending = sum(
            1
            for task in tasks
            if task[4] != COMPLETED
        )

        percentage = (
            int(
                (completed / total) * 100
            )
            if total > 0
            else 0
        )

        content.content = ft.Column(
            spacing=18,
            scroll=ft.ScrollMode.AUTO,
            controls=[

                ft.Text(
                    "STATISTICS",
                    size=25,
                    color=CYAN,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Text(
                    "Your productivity overview",
                    size=13,
                    color=MUTED,
                ),

                ft.Row(
                    spacing=10,
                    controls=[
                        stat_card(
                            "TOTAL",
                            total,
                            ft.Icons.LIST_ALT,
                            CYAN,
                        ),
                        stat_card(
                            "COMPLETED",
                            completed,
                            ft.Icons.CHECK_CIRCLE,
                            GREEN,
                        ),
                    ],
                ),

                ft.Row(
                    spacing=10,
                    controls=[
                        stat_card(
                            "PENDING",
                            pending,
                            ft.Icons.PENDING_ACTIONS,
                            ORANGE,
                        ),
                        stat_card(
                            "SUCCESS",
                            f"{percentage}%",
                            ft.Icons.TRENDING_UP,
                            PURPLE,
                        ),
                    ],
                ),

                ft.Container(
                    padding=20,
                    bgcolor=CARD,
                    border_radius=16,
                    border=ft.Border.all(
                        1,
                        "#18264B",
                    ),
                    content=ft.Column(
                        spacing=15,
                        controls=[
                            ft.Text(
                                "COMPLETION RATE",
                                size=12,
                                color=MUTED,
                                weight=(
                                    ft.FontWeight.BOLD
                                ),
                            ),

                            ft.Text(
                                f"{percentage}%",
                                size=40,
                                color=CYAN,
                                weight=(
                                    ft.FontWeight.BOLD
                                ),
                            ),

                            ft.ProgressBar(
                                value=(
                                    percentage / 100
                                ),
                                color=CYAN,
                                bgcolor="#1B2848",
                                height=10,
                            ),
                        ],
                    ),
                ),

                ft.Text(
                    "TASK HISTORY",
                    size=15,
                    color=WHITE,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Column(
                    spacing=8,
                    controls=[
                        ft.Container(
                            padding=12,
                            bgcolor=CARD,
                            border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.CHECK_CIRCLE,
                                        color=GREEN,
                                    ),
                                    ft.Text(
                                        f"{completed} completed tasks",
                                        color=WHITE,
                                    ),
                                ],
                            ),
                        ),

                        ft.Container(
                            padding=12,
                            bgcolor=CARD,
                            border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.PENDING_ACTIONS,
                                        color=ORANGE,
                                    ),
                                    ft.Text(
                                        f"{pending} pending tasks",
                                        color=WHITE,
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ],
        )

        page.update()

    # ========================================================
    # SETTINGS
    # ========================================================

    def show_settings():

        # ----------------------------------------------------
        # CLEAR COMPLETED
        # ----------------------------------------------------

        def clear_completed(_):

            tasks = get_tasks_list()

            count = 0

            for task in tasks:

                if task[4] == COMPLETED:

                    if remove_a_task(task[0]):
                        count += 1

            show_snack(
                f"{count} completed task(s) removed."
            )

            page.update()

        # ----------------------------------------------------
        # RESET ALL
        # ----------------------------------------------------

        def reset_all(_):

            def confirm_reset(_):

                delete_all_tasks()

                close_dialog(dialog)

                show_snack(
                    "All tasks deleted."
                )

                change_page(0)

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(
                    "Reset All Tasks",
                    color=WHITE,
                ),
                content=ft.Text(
                    "This will permanently delete all tasks.",
                    color=MUTED,
                ),
                actions=[
                    ft.TextButton(
                        "CANCEL",
                        on_click=lambda _: close_dialog(
                            dialog
                        ),
                    ),
                    ft.TextButton(
                        "DELETE ALL",
                        on_click=confirm_reset,
                    ),
                ],
            )

            page.show_dialog(dialog)

        # ----------------------------------------------------
        # ABOUT
        # ----------------------------------------------------

        def about(_):

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(
                    "TASKFLOW",
                    color=CYAN,
                ),
                content=ft.Text(
                    "TaskFlow is an offline task management "
                    "application built with Flet and SQLite.",
                    color=MUTED,
                ),
                actions=[
                    ft.TextButton(
                        "CLOSE",
                        on_click=lambda _: close_dialog(
                            dialog
                        ),
                    ),
                ],
            )

            page.show_dialog(dialog)

        # ----------------------------------------------------
        # SETTINGS SCREEN
        # ----------------------------------------------------

        content.content = ft.Column(
            spacing=18,
            scroll=ft.ScrollMode.AUTO,
            controls=[

                ft.Text(
                    "SETTINGS",
                    size=25,
                    color=CYAN,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Text(
                    "Manage your TaskFlow application",
                    size=13,
                    color=MUTED,
                ),

                ft.Container(
                    padding=18,
                    bgcolor=CARD,
                    border_radius=16,
                    border=ft.Border.all(
                        1,
                        "#18264B",
                    ),
                    content=ft.Column(
                        spacing=5,
                        controls=[

                            ft.Text(
                                "TASK MANAGEMENT",
                                size=11,
                                color=MUTED,
                                weight=(
                                    ft.FontWeight.BOLD
                                ),
                            ),

                            ft.ListTile(
                                leading=ft.Icon(
                                    ft.Icons.CHECK_CIRCLE_OUTLINE,
                                    color=GREEN,
                                ),
                                title=ft.Text(
                                    "Clear completed tasks",
                                    color=WHITE,
                                ),
                                subtitle=ft.Text(
                                    "Remove only completed tasks",
                                    color=MUTED,
                                ),
                                on_click=clear_completed,
                            ),

                            ft.ListTile(
                                leading=ft.Icon(
                                    ft.Icons.DELETE_FOREVER,
                                    color=RED,
                                ),
                                title=ft.Text(
                                    "Reset all tasks",
                                    color=WHITE,
                                ),
                                subtitle=ft.Text(
                                    "Delete every task from the database",
                                    color=MUTED,
                                ),
                                on_click=reset_all,
                            ),
                        ],
                    ),
                ),

                ft.Container(
                    padding=18,
                    bgcolor=CARD,
                    border_radius=16,
                    border=ft.Border.all(
                        1,
                        "#18264B",
                    ),
                    content=ft.ListTile(
                        leading=ft.Icon(
                            ft.Icons.INFO_OUTLINE,
                            color=CYAN,
                        ),
                        title=ft.Text(
                            "About TaskFlow",
                            color=WHITE,
                        ),
                        subtitle=ft.Text(
                            "About this application",
                            color=MUTED,
                        ),
                        on_click=about,
                    ),
                ),
            ],
        )

        page.update()

    # ========================================================
    # ADD TO PAGE
    # ========================================================

    page.navigation_bar = navigation
    page.add(content)

    # ========================================================
    # INITIAL PAGE
    # ========================================================

    show_home()
    page.run_task(
        automatic_status_update
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    ft.run(main)