from django.shortcuts import render
import markdown2
import os
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.shortcuts import redirect
from random import choice

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    content = util.get_entry(entry_name)
    if content == None:
        return redirect('wiki:error', error_description = "entry not found.")
    else:
        return render(request, "encyclopedia/entry.html", {
            "entries": util.list_entries(),
            "entry_name": entry_name,
            "content": markdown2.markdown(content)
        })

def error(request, error_description):
    return render(request, "encyclopedia/error.html",{
        "error_description": error_description
    })

def search(request):
    search_term = request.GET.get('q', '').lower()
    search_results = []
    for entry in util.list_entries():
        if search_term.lower() in entry.lower():
            search_results.append(entry)
    if search_term.lower() in (item.lower() for item in util.list_entries()):
        return HttpResponseRedirect(reverse("wiki:entry", kwargs={'entry_name': search_term}),{
            "search_term": search_term
        })
    return render(request, "encyclopedia/search.html", {
        "search_results": search_results,
        "search_term": search_term
    })


class NewEntryForm(forms.Form):
    entry_name = forms.CharField(label = "Entry Name: ")
    entry_content = forms.CharField(label = "Entry content: ", widget=forms.Textarea(attrs={'name':'body', 'rows':10, 'cols':20}), strip=False)
    

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry_name = form.cleaned_data["entry_name"]
            entry_content = form.cleaned_data["entry_content"]
            if entry_name.lower() not in (item.lower() for item in util.list_entries()):
                with open('entries/'+entry_name+'.md', 'a') as file:
                    file.write('#'+entry_name.capitalize() +'\n '+entry_content)
                return redirect('wiki:entry', entry_name)
            else:
                print("=========")
                return redirect('wiki:error', error_description = "entry already exists on encyclopedia. Not possible to add a new one. Please edit current entry.")
                
    return render(request, "encyclopedia/create.html",{
        "create_form": NewEntryForm
    })

def edit(request):
    if request.method == "GET" and request.GET.get('q') is not None:
        entry = util.get_entry(request.GET.get('q')).lstrip(" #")
        entry_name, entry_content = entry.split("\n", 1)
        form = NewEntryForm(initial={'entry_name':entry_name, 'entry_content':entry_content})
        return render(request, 'encyclopedia/edit.html', {
            'entry_name': entry_name,
            'entry_content': entry_content,
            'form': form
        })
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry_name = form.cleaned_data["entry_name"]
            entry_content = '\n' + form.cleaned_data["entry_content"].replace("\r", "").lstrip()
            print(entry_content)
            if entry_name.lower() in (item.lower() for item in util.list_entries()) and entry_name == request.GET.get('q'):
                with open('entries/'+entry_name+'.md', 'w') as file:
                    file.write('#'+entry_name[0].upper() + entry_name[1:] +'\n '+entry_content)
                return redirect('wiki:entry', entry_name)
            if entry_name.lower() in (item.lower() for item in util.list_entries()) and entry_name != request.GET.get('q'):
                return redirect('wiki:error', error_description = "entry name already exists on encyclopedia. Not possible to change to this name for the edited entry.")
            if entry_name.lower() not in (item.lower() for item in util.list_entries()):
                print("AQUI ESTA O NOME DO ARQUIVO A DELETAR"+request.GET.get('q'))
                os.remove('entries/'+request.GET.get('q')+'.md')
                with open('entries/'+entry_name+'.md', 'w') as file:
                    file.write('#'+entry_name[0].upper() + entry_name[1:] +'\n '+entry_content)
                return redirect('wiki:entry', entry_name)
            
def random(request):
    entries_list = util.list_entries()
    entry_name = choice(entries_list)
    return redirect('wiki:entry', entry_name)