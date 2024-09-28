from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from main.models import Organisaties, Onderzoeken, Beperkingen, Deelnames
from ervaringsdeskundige.models import (
    BeperkingenOnderzoeken,
    )
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from main.serializers import (
    OrganisatieSerializer,
    OnderzoekenSerializer,
    OrganisatiePutSerializer,
    ExperienceExpertSerializer
    )
from rest_framework.response import Response


def index(request):
    return render(request, "home/index_test.html")


def custom_login(request):
    if request.user.is_authenticated and request.user.is_staff == 1:
        return redirect("/beheerder/dashboard")

    if request.user.is_authenticated and request.user.is_staff == 0:
        return redirect("/ervaringsdeskundige/dashboard")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None and user.status == 2:
            auth_login(request, user)
            if request.user.is_authenticated and request.user.is_staff == 1:
                return redirect("/beheerder/dashboard")

            if request.user.is_authenticated and request.user.is_staff == 0:
                return redirect("/ervaringsdeskundige/dashboard")
        else:
            messages.success(request, ("Het inloggen ging fout"))
            return render(request, "home/login.html", {})

    else:
        return render(request, "home/login.html", {})


def register(request):
    return render(request, "home/register.html")


@api_view(["GET", "POST"])
def API(request):
    if request.method == "GET":
        all_organisaties = Organisaties.objects.all()
        serializer = OrganisatieSerializer(all_organisaties, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = OrganisatieSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(["GET", "PUT"])
def organisatie_details(request, pk):
    api_key = request.GET.get("api_key")
    try:
        organistatie = Organisaties.objects.get(pk=pk)
    except Organisaties.DoesNotExist:
        return JsonResponse({"error": "Ongeldige organisatie id"}, status=404)

    if organistatie.api_key != api_key:
        return JsonResponse({"error": "Ongeldige API-key"}, status=403)

    if request.method == "GET":
        serializer = OrganisatieSerializer(organistatie)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        if "organisatie_id" in request.data:
            return JsonResponse(
                {"error": "Not allow to change id"},
                status=403
                )

        old_phone = request.data['telefoonnummer']
        request.data['telefoonnummer'] = int(old_phone.replace(" ", ""))
        serializer = OrganisatiePutSerializer(organistatie, data=request.data)
        if serializer.is_valid():
            serializer.update(organistatie, validated_data=request.data)
            return JsonResponse(serializer.data, status=204)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'PUT'])
def update_onderzoek(request, onderzoeks_id):
    API_key = request.GET.get('api_key')
    try:
        organisation = Organisaties.objects.get(api_key=API_key)
        onderzoek = Onderzoeken.objects.filter(
            organisatie_id=organisation.pk
            ).get(pk=onderzoeks_id)
        limitation_ids = BeperkingenOnderzoeken.objects.filter(
            onderzoeks_id=onderzoek.onderzoeks_id
            ).values_list('beperking_id', flat=True)
        limitations = Beperkingen.objects.filter(id__in=limitation_ids)
        list_attendance_request = Deelnames.objects.filter(
            onderzoeks_id=onderzoeks_id
            ).select_related('ervaringsdeskundige')

        list_limitations_research = []

        for limitation in limitations:
            list_limitations_research.append(limitation.omschrijving)

        list_experts = []
        for attendance in list_attendance_request:
            list_experts.append(attendance.ervaringsdeskundige)

    except Onderzoeken.DoesNotExist or Organisaties.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = OnderzoekenSerializer(onderzoek)
        serializer_experts = ExperienceExpertSerializer(
            list_experts,
            many=True
            )
        data = {
            "omschrijving": serializer.data["omschrijving"],
            "doelgroep_beperking": list_limitations_research,
            "doelgroep_leeftijd_tot": serializer.data[
                "doelgroep_leeftijd_tot"
                ],
            "doelgroep_leeftijd_van": serializer.data[
                "doelgroep_leeftijd_van"
                ],
            "datum_vanaf": serializer.data["datum_vanaf"],
            "datum_tot": serializer.data["datum_tot"],
            "experts": serializer_experts.data,
            "onderzoeks_id": serializer.data["onderzoeks_id"],
            "met_beloning": serializer.data["met_beloning"],
            "titel": serializer.data["titel"],
            "status": serializer.data["status"],
            "type_onderzoek": serializer.data["type_onderzoek"],
        }
        return JsonResponse(data)

    if request.method == 'PUT':
        serializer_context = {'API_key': API_key}
        serializer = OnderzoekenSerializer(
            onderzoek,
            data=request.data,
            partial=True,
            context=serializer_context
            )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@api_view(["GET", "POST"])
def lijst_onderzoeken(request):
    API_key = request.GET.get("api_key")

    if request.method == "GET":
        try:
            organisation = Organisaties.objects.get(api_key=API_key)
            onderzoeken_per_org = Onderzoeken.objects.filter(
                organisatie_id=organisation.organisatie_id
            )
            serializer = OnderzoekenSerializer(onderzoeken_per_org, many=True)
            return JsonResponse(serializer.data, safe=False)

        except Organisaties.DoesNotExist:
            return JsonResponse({"error": "Ongeldige API-key"}, status=400)

    elif request.method == "POST":
        try:
            organisation = Organisaties.objects.get(api_key=API_key)
            serializer = OnderzoekenSerializer(
                data=request.data, organisatie=organisation
            )
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            else:
                print("Validation errors:", serializer.errors)
                return JsonResponse(serializer.errors, status=400)

        except Organisaties.DoesNotExist:
            return JsonResponse({"error": "Ongeldige API-key"}, status=400)

    return Response({"error": "Onverwachte fout"}, status=500)
