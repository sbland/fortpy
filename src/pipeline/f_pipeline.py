from __future__ import print_function, absolute_import, division
import _pipeline
import f90wrap.runtime
import logging

class Config(f90wrap.runtime.FortranModule):
    """
    Module config
    
    
    Defined at config.fpp lines 5-8
    
    """
    @f90wrap.runtime.register_class("pipeline.ConfigShape")
    class ConfigShape(f90wrap.runtime.FortranDerivedType):
        """
        Type(name=configshape)
        
        
        Defined at config.fpp lines 7-8
        
        """
        def __init__(self, handle=None):
            """
            self = Configshape()
            
            
            Defined at config.fpp lines 7-8
            
            
            Returns
            -------
            this : Configshape
            	Object to be constructed
            
            
            Automatically generated constructor for configshape
            """
            f90wrap.runtime.FortranDerivedType.__init__(self)
            result = _pipeline.f90wrap_configshape_initialise()
            self._handle = result[0] if isinstance(result, tuple) else result
        
        def __del__(self):
            """
            Destructor for class Configshape
            
            
            Defined at config.fpp lines 7-8
            
            Parameters
            ----------
            this : Configshape
            	Object to be destructed
            
            
            Automatically generated destructor for configshape
            """
            if self._alloc:
                _pipeline.f90wrap_configshape_finalise(this=self._handle)
        
        @property
        def nl(self):
            """
            Element nl ftype=integer  pytype=int
            
            
            Defined at config.fpp line 8
            
            """
            return _pipeline.f90wrap_configshape__get__nl(self._handle)
        
        @nl.setter
        def nl(self, nl):
            _pipeline.f90wrap_configshape__set__nl(self._handle, nl)
        
        def __str__(self):
            ret = ['<configshape>{\n']
            ret.append('    nl : ')
            ret.append(repr(self.nl))
            ret.append('}')
            return ''.join(ret)
        
        _dt_array_initialisers = []
        
    
    _dt_array_initialisers = []
    

config = Config()

class External_State(f90wrap.runtime.FortranModule):
    """
    Module external_state
    
    
    Defined at external_state.fpp lines 5-8
    
    """
    @f90wrap.runtime.register_class("pipeline.ExternalStateShape")
    class ExternalStateShape(f90wrap.runtime.FortranDerivedType):
        """
        Type(name=externalstateshape)
        
        
        Defined at external_state.fpp lines 7-8
        
        """
        def __init__(self, handle=None):
            """
            self = Externalstateshape()
            
            
            Defined at external_state.fpp lines 7-8
            
            
            Returns
            -------
            this : Externalstateshape
            	Object to be constructed
            
            
            Automatically generated constructor for externalstateshape
            """
            f90wrap.runtime.FortranDerivedType.__init__(self)
            result = _pipeline.f90wrap_externalstateshape_initialise()
            self._handle = result[0] if isinstance(result, tuple) else result
        
        def __del__(self):
            """
            Destructor for class Externalstateshape
            
            
            Defined at external_state.fpp lines 7-8
            
            Parameters
            ----------
            this : Externalstateshape
            	Object to be destructed
            
            
            Automatically generated destructor for externalstateshape
            """
            if self._alloc:
                _pipeline.f90wrap_externalstateshape_finalise(this=self._handle)
        
        @property
        def tsc(self):
            """
            Element tsc ftype=real  pytype=float
            
            
            Defined at external_state.fpp line 8
            
            """
            return _pipeline.f90wrap_externalstateshape__get__tsc(self._handle)
        
        @tsc.setter
        def tsc(self, tsc):
            _pipeline.f90wrap_externalstateshape__set__tsc(self._handle, tsc)
        
        def __str__(self):
            ret = ['<externalstateshape>{\n']
            ret.append('    tsc : ')
            ret.append(repr(self.tsc))
            ret.append('}')
            return ''.join(ret)
        
        _dt_array_initialisers = []
        
    
    _dt_array_initialisers = []
    

external_state = External_State()

class Model_State(f90wrap.runtime.FortranModule):
    """
    Module model_state
    
    
    Defined at model_state.fpp lines 5-8
    
    """
    @f90wrap.runtime.register_class("pipeline.ModelState")
    class ModelState(f90wrap.runtime.FortranDerivedType):
        """
        Type(name=modelstate)
        
        
        Defined at model_state.fpp lines 7-8
        
        """
        def __init__(self, handle=None):
            """
            self = Modelstate()
            
            
            Defined at model_state.fpp lines 7-8
            
            
            Returns
            -------
            this : Modelstate
            	Object to be constructed
            
            
            Automatically generated constructor for modelstate
            """
            f90wrap.runtime.FortranDerivedType.__init__(self)
            result = _pipeline.f90wrap_modelstate_initialise()
            self._handle = result[0] if isinstance(result, tuple) else result
        
        def __del__(self):
            """
            Destructor for class Modelstate
            
            
            Defined at model_state.fpp lines 7-8
            
            Parameters
            ----------
            this : Modelstate
            	Object to be destructed
            
            
            Automatically generated destructor for modelstate
            """
            if self._alloc:
                _pipeline.f90wrap_modelstate_finalise(this=self._handle)
        
        @property
        def hr(self):
            """
            Element hr ftype=real  pytype=float
            
            
            Defined at model_state.fpp line 8
            
            """
            return _pipeline.f90wrap_modelstate__get__hr(self._handle)
        
        @hr.setter
        def hr(self, hr):
            _pipeline.f90wrap_modelstate__set__hr(self._handle, hr)
        
        def __str__(self):
            ret = ['<modelstate>{\n']
            ret.append('    hr : ')
            ret.append(repr(self.hr))
            ret.append('}')
            return ''.join(ret)
        
        _dt_array_initialisers = []
        
    
    _dt_array_initialisers = []
    

model_state = Model_State()

class Pipeline(f90wrap.runtime.FortranModule):
    """
    Module pipeline
    
    
    Defined at pipeline.fpp lines 5-28
    
    """
    @staticmethod
    def hello(val_in):
        """
        outval = hello(val_in)
        
        
        Defined at pipeline.fpp lines 25-28
        
        Parameters
        ----------
        val_in : float
        
        Returns
        -------
        outval : float
        
        """
        outval = _pipeline.f90wrap_hello(val_in=val_in)
        return outval
    
    _dt_array_initialisers = []
    

pipeline = Pipeline()

