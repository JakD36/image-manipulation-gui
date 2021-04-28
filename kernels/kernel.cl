__kernel void pull_sat_from_rgb(__read_only image2d_t src, __write_only image2d_t dest_lum, __write_only image2d_t dest_sat)
{
    const sampler_t sampler =  CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;
    int2 pos = (int2)(get_global_id(0), get_global_id(1));

    float4 rgba = read_imagef(src, sampler, pos);

    float _max = max(max(rgba.r,rgba.g),rgba.b);
    float _min = min(min(rgba.r,rgba.g),rgba.b);

    float lum = (_min + _max) / 2.0f;

    float sat = 0;
    if(_min != _max)
    {
        if (lum > 0.5)
        {
            sat = (_max - _min) / (2.0f - _max - _min);
        }
        else
        {
            sat = (_max - _min) / (_max + _min);
        }
    }


    write_imagef(dest_lum, pos, float4(lum,lum,lum,1.0f));
    write_imagef(dest_sat, pos, float4(sat,sat,sat,1.0f));
}