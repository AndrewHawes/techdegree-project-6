from django.shortcuts import reverse
from django.test import TestCase

from .models import Mineral, DisplayField


def create_mineral(name, all_fields=True):
    if all_fields:
        return Mineral.objects.create(
            name=name,
            image_filename='test.jpg',
            image_caption='caption test',
            category='category test',
            formula='formula test',
            strunz_classification='strunz_test',
            crystal_system='crystal system test',
            unit_cell='unit cell test',
            color='color test',
            crystal_symmetry='crystal symmetry test',
            cleavage='cleavage test',
            mohs_scale_hardness='mohs scale hardness test',
            luster='luster test',
            streak='streak test',
            diaphaneity='diaphaneity test',
            optical_properties='optical properties test',
            refractive_index='refractive index test',
            crystal_habit='crystal habit test',
            specific_gravity='specific gravity test',
            group='group test'
        )
    else:
        return Mineral.objects.create(
            name='name',
            image_filename='test.jpg',
            image_caption='caption test',
            category='category test limited fields',
            formula='formula test limited fields'
        )


class ModelsTests(TestCase):
    def test_display_field_class(self):
        """
        DisplayField returns fields with dot notation accessible field name
        and value.
        """
        gothamite = create_mineral('Gothamite')
        field = DisplayField('formula', gothamite.formula)
        self.assertEqual(field.name, 'formula')
        self.assertEqual(field.value, 'formula test')

    def test_mineral_model_display_fields_all_fields(self):
        """
        Mineral model's display_fields returns list of fields with field names
        and values accessible by dot notation.
        """
        gothamite = create_mineral('Gothamite')
        fields = gothamite.display_fields
        self.assertEqual(len(fields), 17)
        self.assertEqual(fields[4].name, 'crystal system')
        self.assertEqual(fields[4].value, 'crystal system test')

    def test_mineral_model_display_fields_not_all_fields(self):
        """
        Mineral model's display_fields excludes fields without a value.
        """
        gothamite = create_mineral('Gothamite', all_fields=False)
        fields = gothamite.display_fields
        self.assertEqual(len(fields), 2)
        self.assertEqual(fields[0].name, 'category')
        self.assertEqual(fields[0].value, 'category test limited fields')
        self.assertEqual(fields[1].name, 'formula')
        self.assertEqual(fields[1].value, 'formula test limited fields')


class IndexViewTests(TestCase):
    def setUp(self):
        create_mineral('Gothamite')
        create_mineral('Kryptonite')

    def test_mineral_list(self):
        """Index view's queryset is equal to list of created minerals."""
        response = self.client.get(reverse('minerals:index'))
        self.assertQuerysetEqual(
            response.context['mineral_list'],
            ['<Mineral: Gothamite>', '<Mineral: Kryptonite>'],
            ordered=False
        )

    def test_display_minerals(self):
        """Created minerals are listed on the index page."""
        response = self.client.get(reverse('minerals:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Gothamite')
        self.assertContains(response, 'Kryptonite')


class DetailViewTests(TestCase):
    def test_no_wrap(self):
        """
        Display template splits mineral names with multiple variants to prevent
        wrapping on hyphen.
        """
        mineral = create_mineral("Gothamite-(Y), Gothamite-(Ce), Gothamite-(Nd)")
        url = reverse('minerals:detail', args=(mineral.id,))
        response = self.client.get(url)
        self.assertContains(response, 'white-space: nowrap;')

    def test_detail_display_all_fields(self):
        mineral = create_mineral("Gothamite")
        url = reverse('minerals:detail', args=(mineral.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Crystal Habit')

    def test_detail_display_not_all_fields(self):
        mineral = create_mineral("Gothamite", all_fields=False)
        url = reverse('minerals:detail', args=(mineral.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Formula')
        self.assertNotContains(response, 'Crystal Habit')


class RandomMineralViewTests(TestCase):
    def setUp(self):
        mineral_names = [
            'Gothamite',
            'Kryptonite',
            'Gordonite',
            'Ambienite'
        ]
        for mineral_name in mineral_names:
            create_mineral(mineral_name)

    def test_random_mineral_redirects(self):
        """Random mineral returns existing mineral."""
        response = self.client.get(reverse('minerals:random_mineral'))
        self.assertEqual(response.status_code, 302)







