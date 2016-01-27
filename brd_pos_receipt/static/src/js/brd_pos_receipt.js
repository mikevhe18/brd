function brd_pos_receipt(instance, module){

    var PosModelSuper = module.PosModel
    module.PosModel = module.PosModel.extend({
        load_server_data: function(){
            var self = this;
            var loaded = PosModelSuper.prototype.load_server_data.call(this);

            loaded = loaded.then(function(){
                return self.fetch(
                    'res.company',
                    [
                        'currency_id',
                        'email',
                        'website',
                        'company_registry',
                        'vat',
                        'name',
                        'phone',
                        'partner_id',
                        'country_id',
                        'tax_calculation_rounding_method',
                        'logo'
                    ],
                    [['id', '=', self.user.company_id[0]]]
                ).then(function(companies){
                    self.company = companies[0];
                    
                    return self.fetch(
                        'pos.config',
                        ['stock_location_id'],
                        [['id','=', self.pos_session.config_id[0]]]
                    ).then(function(configs){
                        self.config = configs[0];
                        self.config.iface_print_via_proxy2 = self.config.iface_print_via_proxy;

                        self.config.use_proxy = self.config.iface_payment_terminal ||
                                                self.config.iface_electronic_scale ||
                                                self.config.iface_print_via_proxy  ||
                                                self.config.iface_scan_via_proxy   ||
                                                self.config.iface_cashdrawer;
                                                
                        return self.fetch(
                            'stock.location',
                            ['name','partner_id','id'],
                            [['id', '=', self.config.stock_location_id[0]]]
                        ).then(function(locations){
                            self.shop = locations[0];
                            
                            if(self.shop.partner_id)
                            {
                                return self.fetch(
                                    'res.partner',
                                    [
                                        'id',
                                        'name',
                                        'street',
                                        'street2',
                                        'city',
                                        'state_id'
                                    ],
                                    [['id', '=', self.shop.partner_id[0]]]
                                ).then(function(partner){
                                    self.partner_location = partner[0];
                                    
                                    if(self.partner_location)
                                    {
                                        if(self.partner_location.state_id)
                                        {
                                            return self.fetch(
                                                'res.country.state',
                                                [
                                                    'id',
                                                    'name'
                                                ],
                                                [['id', '=', self.partner_location.state_id[0]]]
                                            ).then(function(state){
                                                self.state = state[0];
                                            });
                                        }
                                    }
                                    
                                });
                            }
                            
                        });
                                            
                    });
                    
                });
                
            });
        return loaded;
        },
    })
}

(function(){
    var _super = window.openerp.point_of_sale;
    window.openerp.point_of_sale = function(instance){
        _super(instance);
        var module = instance.point_of_sale;

        brd_pos_receipt(instance, module);
    }
})()
