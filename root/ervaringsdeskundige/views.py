from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ToezichthoudersForm, UserEditForm
from main.models import (
    Onderzoeken,
    Deelnames,
    Beperkingen,
    BeperkingenErvaringsdeskundigen,
    Organisaties,
    TypeOnderzoek,
)
from .models import BeperkingenOnderzoeken
from django.http import JsonResponse, FileResponse
from django.contrib.staticfiles import finders
import datetime


def register(request):
    limitations = Beperkingen.objects.all()
    supervisors_post = ToezichthoudersForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            #lijst uit het formulier ophalen
            selected_limitations = request.POST.getlist("selected_limitations[]")

            #per beperking opslaan als losse rij in de database
            for selected_limitation in selected_limitations:
                ervaringsdeskundige_beperking = BeperkingenErvaringsdeskundigen(
                    beperking_id=int(selected_limitation),
                    ervaringsdeskundigen_id=user.id,
                )
                ervaringsdeskundige_beperking.save()

            type_onderzoek = TypeOnderzoek()
            type_onderzoek.ervaringsdeskundige_id = user.id

            #per type beperking opslaan als losse rij in de database
            type_investigation = request.POST.getlist("type_investigation[]")
            for investigation_type in type_investigation:
                if "Telefonisch" in investigation_type:
                    type_onderzoek.telefonisch = True
                elif "Internet" in investigation_type:
                    type_onderzoek.internet = True
                elif "Locatie" in investigation_type:
                    type_onderzoek.locatie = True

            type_onderzoek.save()

            # dubbelcheck als iemand onder de 18 is wordt toezichthouder opgeslagen
            if (
                user.geboortedatum
                and (datetime.date.today() - user.geboortedatum).days / 365 < 18
            ):
                supervisors_post = ToezichthoudersForm(request.POST)
                if supervisors_post.is_valid():
                    toezichthouder = supervisors_post.save(commit=False)
                    toezichthouder.ervaringsdeskundige = user.id
                    toezichthouder.save()

            return redirect("/")
    else:
        form = RegisterForm()

    return render(
        request,
        "ervaringsdeskundige/register.html",
        {"form": form, "limitations": limitations, "supervisors": supervisors_post},
    )


@login_required()
def dashboard_ervaringsdeskundige(request):
    current_user = request.user

    user_id = request.user.id

    # haal de data op voor lopende onderzoeken
    current_investigations = Deelnames.objects.filter(
        ervaringsdeskundige_id=user_id
    ).filter(status=2)

    investigation_ids = current_investigations.values_list("onderzoeks_id", flat=True)

    investigations = Onderzoeken.objects.filter(onderzoeks_id__in=investigation_ids)

    investigations_with_limitations = {}

    for investigation in investigations:
        limitation_ids = BeperkingenOnderzoeken.objects.filter(
            onderzoeks_id=investigation.onderzoeks_id
        ).values_list("beperking_id", flat=True)

        limitations = Beperkingen.objects.filter(id__in=limitation_ids)

        investigations_with_limitations[investigation.onderzoeks_id] = {
            "onderzoek": investigation,
            "beperkingen": limitations,
        }



    # haal de data voor lopende onderzoeken
    current_investigations_2 = Deelnames.objects.filter(
        ervaringsdeskundige_id=user_id
    ).filter(status=4)

    investigation_ids_2 = current_investigations_2.values_list(
        "onderzoeks_id", flat=True
    )

    investigations_2 = Onderzoeken.objects.filter(onderzoeks_id__in=investigation_ids_2)

    investigations_with_limitations_2 = {}

    # haal daarbij elke losse rij met beperking op voor het onderzoek
    for investigation in investigations_2:
        limitation_ids = BeperkingenOnderzoeken.objects.filter(
            onderzoeks_id=investigation.onderzoeks_id
        ).values_list("beperking_id", flat=True)

        limitations = Beperkingen.objects.filter(id__in=limitation_ids)

        investigations_with_limitations_2[investigation.onderzoeks_id] = {
            "onderzoek": investigation,
            "beperkingen": limitations,
        }

    return render(
        request,
        "ervaringsdeskundige/dashboard.html",
        {
            "user": current_user,
            "ongoing_investigations": investigations_with_limitations,
            "finished_investigations": investigations_with_limitations_2,
        },
    )


@login_required
def edit_profile(request):
    current_user = request.user

    if request.method == "POST":
        form = UserEditForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            return redirect("/ervaringsdeskundige/dashboard")
        print(form.errors)
    else:
        form = UserEditForm(instance=current_user)

    return render(request, "ervaringsdeskundige/edit_profile.html", {"form": form})


@login_required()
def logout_ervaringsdeskundige(request):
    logout(request)
    return redirect("/login")


@login_required
def onderzoeken(request):
    user = request.user
    user_age = user.age()
    user_available_from = user.beschikbaar_vanaf
    user_available_until = user.beschikbaar_tot
    limitations_user = BeperkingenErvaringsdeskundigen.objects.filter(
        ervaringsdeskundigen_id=user.id
    )

    limitations_ids = limitations_user.values_list("beperking_id", flat=True)

    filtered_investigations = BeperkingenOnderzoeken.objects.filter(
        beperking_id__in=limitations_ids
    )
    filtered_investigations_ids = filtered_investigations.values_list(
        "onderzoeks_id", flat=True
    )

    investigations = Onderzoeken.objects.filter(
        doelgroep_leeftijd_van__lte=user_age,
        doelgroep_leeftijd_tot__gte=user_age,
        datum_vanaf__lte=user_available_until,
        datum_tot__gte=user_available_from,
        onderzoeks_id__in=filtered_investigations_ids,
    )

    investigations_with_limitations = {}

    for investigation in investigations:
        limitation_ids = BeperkingenOnderzoeken.objects.filter(
            onderzoeks_id=investigation.onderzoeks_id
        ).values_list("beperking_id", flat=True)

        limitations = Beperkingen.objects.filter(id__in=limitation_ids)
        existing = Deelnames.objects.filter(
            ervaringsdeskundige_id=user.id, onderzoeks_id=investigation.onderzoeks_id
        ).first()

        status = 0
        if existing and existing.status == 1:
            status = 1

        if existing and existing.status == 2:
            status = 2

        investigations_with_limitations[investigation.onderzoeks_id] = {
            "onderzoek": investigation,
            "beperkingen": limitations,
            "status": status,
        }

    return render(
        request,
        "ervaringsdeskundige/onderzoeken.html",
        {"investigations": investigations_with_limitations},
    )



@login_required
def registered_investigations(request):
    user_id = request.user.id

    current_investigations = Deelnames.objects.filter(
        ervaringsdeskundige_id=user_id
    ).filter(status=1)

    investigation_ids = current_investigations.values_list("onderzoeks_id", flat=True)

    investigations = Onderzoeken.objects.filter(onderzoeks_id__in=investigation_ids)

    investigations_with_limitations = {}

    for investigation in investigations:
        limitation_ids = BeperkingenOnderzoeken.objects.filter(
            onderzoeks_id=investigation.onderzoeks_id
        ).values_list("beperking_id", flat=True)

        limitations = Beperkingen.objects.filter(id__in=limitation_ids)

        investigations_with_limitations[investigation.onderzoeks_id] = {
            "onderzoek": investigation,
            "beperkingen": limitations,
        }

    return render(
        request,
        "ervaringsdeskundige/registered_investigations.html",
        {"investigations": investigations_with_limitations},
    )


@login_required
def completed_investigations(request):
    user_id = request.user.id

    current_investigations = Deelnames.objects.filter(
        ervaringsdeskundige_id=user_id
    ).filter(status=4)

    investigation_ids = current_investigations.values_list("onderzoeks_id", flat=True)

    investigations = Onderzoeken.objects.filter(onderzoeks_id__in=investigation_ids)

    investigations_with_limitations = {}

    for investigation in investigations:
        limitation_ids = BeperkingenOnderzoeken.objects.filter(
            onderzoeks_id=investigation.onderzoeks_id
        ).values_list("beperking_id", flat=True)

        limitations = Beperkingen.objects.filter(id__in=limitation_ids)

        investigations_with_limitations[investigation.onderzoeks_id] = {
            "onderzoek": investigation,
            "beperkingen": limitations,
        }

    return render(
        request,
        "ervaringsdeskundige/completed_investigations.html",
        {"investigations": investigations_with_limitations},
    )


@login_required
def register_investigation(request, investigation_id):
    user_id = request.user.id

    existing = Deelnames.objects.filter(
        ervaringsdeskundige_id=user_id, onderzoeks_id=investigation_id
    )

    if not existing:
        new_register_investigation = Deelnames(
            ervaringsdeskundige_id=user_id,
            onderzoeks_id=investigation_id,
            status=1,
            contact=0,
        )
        new_register_investigation.save()

    return redirect("/ervaringsdeskundige/register_investigation_succes")


@login_required
def register_investigation_succes(request):
    return render(request, "ervaringsdeskundige/register_investigation_succes.html")


@login_required
def unsubscribe_investigation(request, investigation_id):
    user_id = request.user.id
    investigation_delete = Deelnames.objects.filter(
        ervaringsdeskundige_id=user_id, onderzoeks_id=investigation_id
    )
    investigation_delete.delete()
    return render(request, "ervaringsdeskundige/unsubscribe_investigation.html")


@login_required
def delete_account(request):
    comment = request.GET.get("comment")
    request.user.opmerking_verwijderd = comment
    request.user.status = 5
    request.user.save()
    logout(request)
    return redirect("/")


@login_required
def live_dashboard_data(request):
    user_id = request.user.id

    investigation_ids = Deelnames.objects.filter(
        ervaringsdeskundige_id=user_id
    ).values_list("onderzoeks_id", flat=True)

    investigations = Onderzoeken.objects.filter(onderzoeks_id__in=investigation_ids)
    registered_investigations_list = {}

    count_status_1 = Deelnames.objects.filter(
        ervaringsdeskundige_id=user_id, status=4
    ).count()
    count_status_2 = Deelnames.objects.filter(
        ervaringsdeskundige_id=user_id, status=1
    ).count()
    count_status_3 = Deelnames.objects.filter(
        ervaringsdeskundige_id=user_id, status=2
    ).count()

    for investigation in investigations:
        deelname = Deelnames.objects.get(
            ervaringsdeskundige_id=user_id, onderzoeks_id=investigation.onderzoeks_id
        )
        status = deelname.status

        registered_investigations_list[investigation.onderzoeks_id] = {
            "onderzoek": {
                "id": investigation.onderzoeks_id,
                "titel": investigation.titel,
            },
            "status": status,
        }

    data = {
        "status": request.user.status,
        "registered_investigations": registered_investigations_list,
        "count_status_1": count_status_1,
        "count_status_2": count_status_2,
        "count_status_3": count_status_3,
    }

    return JsonResponse(data)


@login_required
def notification(request):
    mp3_file_path = finders.find("sounds/notification.mp3")

    if mp3_file_path:
        response = FileResponse(open(mp3_file_path, "rb"), content_type="audio/mpeg")
        return response


@login_required
def inspect_investigation(request, investigation_id):
    investigations = Onderzoeken.objects.filter(onderzoeks_id=investigation_id)

    investigations_with_limitations = {}

    for investigation in investigations:
        limitation_ids = BeperkingenOnderzoeken.objects.filter(
            onderzoeks_id=investigation.onderzoeks_id
        ).values_list("beperking_id", flat=True)

        limitations = Beperkingen.objects.filter(id__in=limitation_ids)

        organisation_id = investigation.organisatie_id
        organisation = Organisaties.objects.filter(
            organisatie_id=organisation_id
        ).first()

        limitations = Beperkingen.objects.filter(id__in=limitation_ids)

        type_investigation = TypeOnderzoek.objects.filter(
            onderzoeks_id=investigation_id
        ).first()
        investigations_with_limitations[investigation.onderzoeks_id] = {
            "onderzoek": investigation,
            "beperkingen": limitations,
            "organisatie": organisation,
            "type_onderzoek": type_investigation,
        }

    return render(
        request,
        "ervaringsdeskundige/inspect_investigation.html",
        {"investigations": investigations_with_limitations},
    )
