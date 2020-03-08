namespace ANONYMOUS{

void main__Wrapper() {
  _main();
}
void main__WrapperNospec() {}
void _main() {
  list::List<int > *  a_s11=NULL;
  list::empty(a_s11);
  list::List<int > *  res_a_s13=NULL;
  list::empty(res_a_s13);
  list::List<int > *  b_s15=NULL;
  list::add(a_s11, 3, b_s15);
  list::List<int > *  b_s17=NULL;
  list::add(b_s15, -4, b_s17);
  list::List<int > *  b_s19=NULL;
  list::add(b_s17, 5, b_s19);
  list::List<int > *  res_b_s21=NULL;
  list::add(a_s11, 3, res_b_s21);
  list::List<int > *  res_b_s23=NULL;
  list::add(res_b_s21, 5, res_b_s23);
  list::List<int > *  c_s25=NULL;
  list::add(a_s11, 16, c_s25);
  list::List<int > *  c_s27=NULL;
  list::add(c_s25, 14, c_s27);
  list::List<int > *  c_s29=NULL;
  list::add(c_s27, -5, c_s29);
  list::List<int > *  c_s31=NULL;
  list::add(c_s29, 1, c_s31);
  list::List<int > *  res_c_s33=NULL;
  list::add(a_s11, 16, res_c_s33);
  list::List<int > *  res_c_s35=NULL;
  list::add(res_c_s33, 14, res_c_s35);
  list::List<int > *  res_c_s37=NULL;
  list::add(res_c_s35, 1, res_c_s37);
  list::List<int > *  d_s39=NULL;
  list::add(a_s11, -18, d_s39);
  list::List<int > *  d_s41=NULL;
  list::add(d_s39, 14, d_s41);
  list::List<int > *  d_s43=NULL;
  list::add(d_s41, 15, d_s43);
  list::List<int > *  d_s45=NULL;
  list::add(d_s43, -10, d_s45);
  list::List<int > *  res_d_s47=NULL;
  list::add(a_s11, 14, res_d_s47);
  list::List<int > *  res_d_s49=NULL;
  list::add(res_d_s47, 15, res_d_s49);
  list::List<int > *  _out_s51=NULL;
  mypos(a_s11, _out_s51);
  bool  _out_s53=0;
  equals_List_s0(_out_s51, res_a_s13, 6, _out_s53);
  assert (_out_s53);;
  list::List<int > *  _out_s55=NULL;
  mypos(b_s19, _out_s55);
  bool  _out_s57=0;
  equals_List_s0(_out_s55, res_b_s23, 6, _out_s57);
  assert (_out_s57);;
  list::List<int > *  _out_s59=NULL;
  mypos(c_s31, _out_s59);
  bool  _out_s61=0;
  equals_List_s0(_out_s59, res_c_s37, 6, _out_s61);
  assert (_out_s61);;
  list::List<int > *  _out_s63=NULL;
  mypos(d_s45, _out_s63);
  bool  _out_s65=0;
  equals_List_s0(_out_s63, res_d_s49, 6, _out_s65);
  assert (_out_s65);;
}
void mypos(list::List<int> * a, list::List<int> *& _out) {
  list::List<int > *  _out_s67=NULL;
  empty_list(_out_s67);
  bool  _out_s69=0;
  equals_List_s0(a, _out_s67, 6, _out_s69);
  if (_out_s69) {
    list::List<int > *  _out_s83=NULL;
    empty_list(_out_s83);
    _out = _out_s83;
    return;
  } else {
    list::List<int > *  _out_s73=NULL;
    ifelist(a, _out_s73);
    _out = _out_s73;
    return;
  }
}
void equals_List_s0(list::List<int > * left_s1, list::List<int > * right_s2, int bnd_s3, bool& _out) {
  if ((bnd_s3) <= (0)) {
    _out = 0;
    return;
  }
  if (((left_s1) == (NULL)) && ((right_s2) == (NULL))) {
    _out = 1;
    return;
  }
  if ((left_s1) == (NULL)) {
    _out = 0;
    return;
  }
  if ((right_s2) == (NULL)) {
    _out = 0;
    return;
  }
  switch(left_s1->type){
  case list::Cons<int >::CONS_type:
    {
    list::Cons<int > *  _left_s1 = (list::Cons<int > * )  left_s1;

    switch(right_s2->type){
    case list::Cons<int >::CONS_type:
        {
        list::Cons<int > *  _right_s2 = (list::Cons<int > * )  right_s2;

      bool  _pac_sc_s7=(_left_s1->val) == (_right_s2->val);
      if (_pac_sc_s7) {
        bool  _pac_sc_s7_s9=0;
        equals_List_s0(_left_s1->next, _right_s2->next, bnd_s3 - 1, _pac_sc_s7_s9);
        _pac_sc_s7 = _pac_sc_s7_s9;
      }
      _out = _pac_sc_s7;
      return;
    
        break;
    }
    default:
        {
        
      _out = 0;
      return;
    
        break;
    }

 }
  
    break;
  }
  case list::Nil<int >::NIL_type:
    {
    list::Nil<int > *  _left_s1 = (list::Nil<int > * )  left_s1;

    switch(right_s2->type){
    case list::Nil<int >::NIL_type:
        {
        list::Nil<int > *  _right_s2 = (list::Nil<int > * )  right_s2;

      _out = 1;
      return;
    
        break;
    }
    default:
        {
        
      _out = 0;
      return;
    
        break;
    }

 }
  
    break;
  }

 }
}
void empty_list(list::List<int > *& _out) {
  list::List<int > *  _out_s99=NULL;
  list::empty(_out_s99);
  _out = _out_s99;
  return;
}
void ifelist(list::List<int > * a, list::List<int > *& _out) {
  int  _out_s95=0;
  list::head(a, _out_s95);
  if ((_out_s95) > (0)) {
    list::List<int > *  _out_s85=((list::Cons<int > *)(a))->next;
    list::List<int > *  _out_s87=NULL;
    mypos(_out_s85, _out_s87);
    int  _out_s95_0=0;
    list::head(a, _out_s95_0);
    list::List<int > *  _out_s93=NULL;
    list::add(_out_s87, _out_s95_0, _out_s93);
    _out = _out_s93;
    return;
  } else {
    list::List<int > *  _out_s85_0=((list::Cons<int > *)(a))->next;
    list::List<int > *  _out_s87_0=NULL;
    mypos(_out_s85_0, _out_s87_0);
    _out = _out_s87_0;
    return;
  }
}

}
namespace list{

template<typename T>
Cons<T>* Cons<T>::create(T  val_, List<T > *  next_){
  void* temp= malloc( sizeof(Cons<T>)  ); 
  Cons<T>* rv = new (temp)Cons<T>();
  rv->val =  val_;
  rv->next =  next_;
  rv->type= List<T>::CONS_type;
  return rv;
}
template<typename T>
Nil<T>* Nil<T>::create(){
  void* temp= malloc( sizeof(Nil<T>)  ); 
  Nil<T>* rv = new (temp)Nil<T>();
  rv->type= List<T>::NIL_type;
  return rv;
}
template<typename T>
void empty(List<T > *& _out) {
  _out = Nil<T >::create();
  return;
}
template<typename T>
void add(List<T > * lst, T val, List<T > *& _out) {
  _out = Cons<T >::create(val, lst);
  return;
}
template<typename T>
void head(List<T > * l, T& _out) {
  _out = ((Cons<T > *)(l))->val;
  return;
}

}
