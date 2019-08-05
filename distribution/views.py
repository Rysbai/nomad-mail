from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from distribution.forms import DistributionCreateForm


def create_distribution(request):
    args = dict()
    args.update(csrf(request))

    distribution_form = DistributionCreateForm(request.POST)
    if distribution_form.is_valid():
        distribution_form.save()
        return redirect('/admin/distribution/distribution')
    else:
        args['form'] = distribution_form
        return render(request, 'admin/distribution/distribution/add', args)

