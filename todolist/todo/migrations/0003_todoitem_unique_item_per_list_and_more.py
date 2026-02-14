from django.db import migrations, models
from django.db.models import Count
from django.db.models.functions import Lower


def remove_duplicates(apps, schema_editor):
    TodoList = apps.get_model("todo", "TodoList")
    TodoItem = apps.get_model("todo", "TodoItem")

    # 🔹 Remove duplicate TodoLists per user
    dupe_lists = (
        TodoList.objects
        .annotate(name_l=Lower("name"))
        .values("user_id", "name_l")
        .annotate(c=Count("id"))
        .filter(c__gt=1)
    )

    for d in dupe_lists:
        qs = TodoList.objects.filter(
            user_id=d["user_id"],
            name__iexact=d["name_l"]
        ).order_by("id")
        qs.exclude(id=qs.first().id).delete()

    # 🔹 Remove duplicate TodoItems per list
    dupe_items = (
        TodoItem.objects
        .annotate(title_l=Lower("title"))
        .values("todo_list_id", "title_l")
        .annotate(c=Count("id"))
        .filter(c__gt=1)
    )

    for d in dupe_items:
        qs = TodoItem.objects.filter(
            todo_list_id=d["todo_list_id"],
            title__iexact=d["title_l"]
        ).order_by("id")
        qs.exclude(id=qs.first().id).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0002_delete_loginuser_delete_signupuser_todolist_user"),
    ]

    operations = [
        migrations.RunPython(remove_duplicates),

        migrations.AddConstraint(
            model_name="todolist",
            constraint=models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_todolist_per_user",
            ),
        ),

        migrations.AddConstraint(
            model_name="todoitem",
            constraint=models.UniqueConstraint(
                fields=["todo_list", "title"],
                name="unique_item_per_list",
            ),
        ),
    ]