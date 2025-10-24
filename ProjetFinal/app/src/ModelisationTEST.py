import pytest
import numpy as np
from Modelisation import calculerCaloriesMET, MET_VALUES


# Fixtures
@pytest.fixture
def duree_normale():
    """Fixture for normal duration in minutes"""
    return 60.0


@pytest.fixture
def poids_normal():
    """Fixture for normal weight in kg"""
    return 70.0


@pytest.fixture
def activites_valides():
    """Fixture for valid activities"""
    return ['course', 'velo', 'natation']


@pytest.fixture
def parametres_realistes():
    """Fixture for realistic test parameters"""
    return [
        ('course', 60.0, 70.0),
        ('velo', 90.0, 65.0),
        ('natation', 45.0, 80.0),
        ('course', 30.0, 75.0),
        ('velo', 120.0, 80.0)
    ]


class TestCalculerCaloriesMET:
    """Test suite for calculerCaloriesMET function"""
    
    def test_course_calcul_normal(self, duree_normale, poids_normal):
        """Test calories calculation for running with normal values"""
        activite = "course"
        
        expected = MET_VALUES['course'] * 3.5 * poids_normal / 200 * duree_normale
        result = calculerCaloriesMET(activite, duree_normale, poids_normal)
        
        assert np.isclose(result, expected)
    
    def test_velo_calcul_normal(self):
        """Test calories calculation for cycling with normal values"""
        activite = "velo"
        duree = 45.0
        poids = 65.0
        
        expected = MET_VALUES['velo'] * 3.5 * poids / 200 * duree
        result = calculerCaloriesMET(activite, duree, poids)
        
        assert np.isclose(result, expected)
    
    def test_natation_calcul_normal(self):
        """Test calories calculation for swimming with normal values"""
        activite = "natation"
        duree = 30.0
        poids = 80.0
        
        expected = MET_VALUES['natation'] * 3.5 * poids / 200 * duree
        result = calculerCaloriesMET(activite, duree, poids)
        
        assert np.isclose(result, expected)
    
    def test_toutes_activites_valides(self, activites_valides, duree_normale, poids_normal):
        """Test that all valid activities return positive calories"""
        for activite in activites_valides:
            result = calculerCaloriesMET(activite, duree_normale, poids_normal)
            assert result > 0
            assert isinstance(result, float)
    
    def test_case_insensitive(self, duree_normale, poids_normal):
        """Test that activity name is case insensitive"""
        result_lower = calculerCaloriesMET("course", duree_normale, poids_normal)
        result_upper = calculerCaloriesMET("COURSE", duree_normale, poids_normal)
        result_mixed = calculerCaloriesMET("Course", duree_normale, poids_normal)
        
        assert np.isclose(result_lower, result_upper)
        assert np.isclose(result_lower, result_mixed)
    
    def test_duree_zero(self, poids_normal):
        """Test with zero duration"""
        result = calculerCaloriesMET("course", 0.0, poids_normal)
        assert result == 0.0
    
    def test_poids_zero(self, duree_normale):
        """Test with zero weight"""
        result = calculerCaloriesMET("velo", duree_normale, 0.0)
        assert result == 0.0
    
    def test_duree_et_poids_zero(self):
        """Test with both zero duration and weight"""
        result = calculerCaloriesMET("natation", 0.0, 0.0)
        assert result == 0.0
    
    def test_activite_inconnue(self, duree_normale, poids_normal):
        """Test that unknown activity raises ValueError"""
        with pytest.raises(ValueError, match="Activité inconnue"):
            calculerCaloriesMET("marche", duree_normale, poids_normal)
    
    def test_activite_vide(self, duree_normale, poids_normal):
        """Test that empty activity raises ValueError"""
        with pytest.raises(ValueError, match="Activité inconnue"):
            calculerCaloriesMET("", duree_normale, poids_normal)
    
    def test_formule_precision(self):
        """Test the precision of the MET formula"""
        activite = "course"
        duree = 30.0
        poids = 75.0
        
        expected = 9.8 * 3.5 * 75.0 / 200 * 30.0
        result = calculerCaloriesMET(activite, duree, poids)
        
        assert result == expected
    
    @pytest.mark.parametrize("activite,duree,poids", [
        ("course", 60.0, 70.0),
        ("velo", 90.0, 65.0),
        ("natation", 45.0, 80.0),
        ("course", 30.0, 75.0),
        ("velo", 120.0, 80.0)
    ])
    def test_valeurs_realistes_parametrize(self, activite, duree, poids):
        """Test with realistic values using parametrize"""
        result = calculerCaloriesMET(activite, duree, poids)
        assert result > 0
        assert isinstance(result, float)
    
    def test_valeurs_realistes_fixture(self, parametres_realistes):
        """Test with realistic values using fixture"""
        for activite, duree, poids in parametres_realistes:
            result = calculerCaloriesMET(activite, duree, poids)
            assert result > 0
            assert isinstance(result, float)
    
    def test_comparaison_activites(self, duree_normale, poids_normal):
        """Test that course burns more calories than velo for same parameters"""
        result_course = calculerCaloriesMET("course", duree_normale, poids_normal)
        result_velo = calculerCaloriesMET("velo", duree_normale, poids_normal)
        result_natation = calculerCaloriesMET("natation", duree_normale, poids_normal)
        
        # Course a le MET le plus élevé (9.8)
        assert result_course > result_natation > result_velo
    
    def test_proportionnalite_duree(self, poids_normal):
        """Test that calories are proportional to duration"""
        activite = "course"
        duree1 = 30.0
        duree2 = 60.0
        
        result1 = calculerCaloriesMET(activite, duree1, poids_normal)
        result2 = calculerCaloriesMET(activite, duree2, poids_normal)
        
        assert np.isclose(result2, 2 * result1)
    
    def test_proportionnalite_poids(self, duree_normale):
        """Test that calories are proportional to weight"""
        activite = "velo"
        poids1 = 50.0
        poids2 = 100.0
        
        result1 = calculerCaloriesMET(activite, duree_normale, poids1)
        result2 = calculerCaloriesMET(activite, duree_normale, poids2)
        
        assert np.isclose(result2, 2 * result1)