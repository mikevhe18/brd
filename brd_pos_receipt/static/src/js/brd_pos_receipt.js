function brd_pos_receipt(instance, module){

    var PosModelSuper = module.PosModel
    module.PosModel = module.PosModel.extend({
        load_server_data: function(){
            var self = this;
            var loaded = PosModelSuper.prototype.load_server_data.call(this);

            loaded = loaded.then(function(){
                return self.fetch(
                    'res.company',
                    ['logo'],
                    {}
                );

            }).then(function(companies){
                self.company = companies[0];
            })
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

        //$('<link rel="stylesheet" href="/pos_ticket_custom/static/src/css/pos.css"/>').appendTo($("head"))
    }
})()
